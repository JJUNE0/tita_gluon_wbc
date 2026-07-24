from __future__ import annotations

import math
import select
import sys
import termios
import time
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import String


class _AxisSlewState:
    """Per-axis state for the stop-only fixed-duration decel in ``_slew_toward``."""

    __slots__ = ("stopping", "stop_start_val", "stop_start_time")

    def __init__(self) -> None:
        self.stopping = False
        self.stop_start_val = 0.0
        self.stop_start_time = 0.0


class KeyboardCommandNode(Node):
    KEY_TO_STATE = {
        "0": "rl_0",
        "1": "reference_transform_up",
        "6": "idle",
        "7": "transform_up",
        "8": "transform_down",
        "9": "joint_pd",
        "5": "wheel_test",
    }

    def __init__(self) -> None:
        super().__init__("cosim_keyboard_command")
        self.declare_parameter("tita_ns", "tita")
        self.declare_parameter("idle_timeout_s", 0.3)
        # Matches My24's training-time command ramp (RampedVelocityCommand,
        # ramp_rate=0.5 units/s -- 1 m/s reached/shed in 2s) so a released key
        # decays the command at the same rate the policy was actually trained
        # on, instead of snapping straight to zero.
        self.declare_parameter("idle_decay_rate", 0.5)
        # Safety: regardless of idle_decay_rate (which governs accel and
        # non-stop target changes), any transition where the target drops to
        # zero (idle-timeout or 'r' reset) always decays linearly to zero in
        # exactly this many seconds, independent of the speed at the moment
        # the stop begins -- a fast command doesn't take proportionally
        # longer to stop.
        self.declare_parameter("stop_decel_time_s", 0.5)
        tita_ns = str(self.get_parameter("tita_ns").value).strip("/") or "tita"
        self.idle_timeout_s = float(self.get_parameter("idle_timeout_s").value)
        self.idle_decay_rate = float(self.get_parameter("idle_decay_rate").value)
        self.stop_decel_time_s = float(self.get_parameter("stop_decel_time_s").value)
        self.key_pub = self.create_publisher(String, f"/{tita_ns}/command/manager/cmd_key", 10)
        self.twist_pub = self.create_publisher(Twist, f"/{tita_ns}/command/manager/cmd_twist", 10)
        # `target_twist`: the operator's desired setpoint, jumps by 0.05 per
        # keypress (or snaps to zero on idle-timeout/reset) exactly as before.
        # `twist`: the actually-published command, slewed toward
        # `target_twist`. For any non-stop transition, at `idle_decay_rate`
        # units/s -- mirrors training's `RampedVelocityCommand` (target vs.
        # emitted, see My24 in Experiments/RL_Experiments.md) so the policy
        # sees similar command dynamics in sim2sim as it was trained on.
        # Whenever the target is zero (idle-timeout/reset -> a stop), this is
        # overridden by the fixed `stop_decel_time_s` safety decay instead
        # (see `_slew_toward`) -- deploy-only, not mirrored in training.
        self.target_twist = Twist()
        self.twist = Twist()
        self._vx_slew_state = _AxisSlewState()
        self._wz_slew_state = _AxisSlewState()
        self.timer = self.create_timer(0.02, self._publish_twist)
        self.get_logger().info(
            "Keys: 1 reference_transform_up, 7 transform_up, 0 rl_0, "
            "6 idle, 9 joint_pd, 5 wheel_test, "
            "w/s vx, a/d wz, r reset, Ctrl-C quit -- "
            f"vx/wz auto-zero after {self.idle_timeout_s:.2f}s of no w/s/a/d, "
            f"slewed at {self.idle_decay_rate:.2f} units/s (matches training's command ramp), "
            f"stop always takes {self.stop_decel_time_s:.2f}s regardless of speed (safety)"
        )

    def _publish_twist(self) -> None:
        self.twist_pub.publish(self.twist)

    def _slew_toward(self, current: float, target: float, dt: float, now: float, state: _AxisSlewState) -> float:
        if target == 0.0:
            # Stopping: always reach zero in exactly stop_decel_time_s,
            # linearly from whatever value the axis had when the stop began
            # -- independent of idle_decay_rate and of how large that value
            # was, so a fast command doesn't take proportionally longer to
            # stop.
            if not state.stopping:
                state.stopping = True
                state.stop_start_val = current
                state.stop_start_time = now
            if self.stop_decel_time_s <= 0.0:
                return 0.0
            frac = min((now - state.stop_start_time) / self.stop_decel_time_s, 1.0)
            return state.stop_start_val * (1.0 - frac)

        state.stopping = False
        max_step = self.idle_decay_rate * dt
        delta = target - current
        if abs(delta) <= max_step:
            return target
        return current + math.copysign(max_step, delta)

    def spin_keyboard(self) -> None:
        input_stream = sys.stdin
        input_close = False
        if not input_stream.isatty():
            try:
                input_stream = open("/dev/tty", "rb", buffering=0)
                input_close = True
            except OSError as exc:
                raise RuntimeError(
                    "Keyboard command node needs a controlling TTY. "
                    "Run it from a terminal or use ros2 run / an interactive shell."
                ) from exc

        old = termios.tcgetattr(input_stream.fileno())
        # last time a w/s/a/d key was seen -- if none arrive for idle_timeout_s,
        # vx/wz snap back to 0 without needing to press 'r'. Terminal key-repeat
        # has an initial delay (~0.2-0.5s) before repeating, so idle_timeout_s
        # must stay comfortably above that or a held key will visibly stutter.
        last_move_key_time = time.monotonic()
        last_loop_time = time.monotonic()
        poll_interval_s = 0.05
        try:
            tty.setcbreak(input_stream.fileno())
            while rclpy.ok():
                ready, _, _ = select.select([input_stream], [], [], poll_interval_s)
                if ready:
                    key = input_stream.read(1)
                    if isinstance(key, bytes):
                        key = key.decode(errors="ignore")
                    if key == "\x03":
                        break
                    if key in self.KEY_TO_STATE:
                        self.key_pub.publish(String(data=self.KEY_TO_STATE[key]))
                    elif key == "w":
                        self.target_twist.linear.x += 0.05
                        last_move_key_time = time.monotonic()
                    elif key == "s":
                        self.target_twist.linear.x -= 0.05
                        last_move_key_time = time.monotonic()
                    elif key == "a":
                        self.target_twist.angular.z += 0.05
                        last_move_key_time = time.monotonic()
                    elif key == "d":
                        self.target_twist.angular.z -= 0.05
                        last_move_key_time = time.monotonic()
                    elif key == "r":
                        self.target_twist = Twist()
                        last_move_key_time = time.monotonic()
                    self.target_twist.linear.x = max(-1.0, min(1.0, self.target_twist.linear.x))
                    self.target_twist.angular.z = max(-0.3, min(0.3, self.target_twist.angular.z))

                now = time.monotonic()
                dt = now - last_loop_time
                last_loop_time = now
                if now - last_move_key_time > self.idle_timeout_s:
                    self.target_twist.linear.x = 0.0
                    self.target_twist.angular.z = 0.0

                # slew the published command toward the target: idle_decay_rate
                # units/s for accel and non-stop changes (matching training's
                # RampedVelocityCommand, My24 -- a raw per-keypress jump fed
                # the policy steeper transitions than trained on, causing the
                # shoulder shake); a fixed stop_decel_time_s-second linear
                # decay whenever the target is zero (idle-timeout/reset),
                # independent of speed, as a deploy-only safety measure.
                self.twist.linear.x = self._slew_toward(
                    self.twist.linear.x, self.target_twist.linear.x, dt, now, self._vx_slew_state
                )
                self.twist.angular.z = self._slew_toward(
                    self.twist.angular.z, self.target_twist.angular.z, dt, now, self._wz_slew_state
                )

                rclpy.spin_once(self, timeout_sec=0.0)
        finally:
            termios.tcsetattr(input_stream.fileno(), termios.TCSADRAIN, old)
            if input_close:
                input_stream.close()


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = KeyboardCommandNode()
    try:
        node.spin_keyboard()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
