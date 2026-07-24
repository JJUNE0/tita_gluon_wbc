from __future__ import annotations

import math

import rclpy
from geometry_msgs.msg import PoseStamped, Twist
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String


def _quat_from_rpy(roll: float, pitch: float, yaw: float) -> tuple[float, float, float, float]:
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    return w, x, y, z


class TitaJoyBridgeNode(Node):
    """Bridge /joy into manual-compatible TITA command-manager topics."""

    def __init__(self) -> None:
        super().__init__("tita_joy_bridge")
        self.declare_parameter("tita_ns", "tita")
        self.declare_parameter("joy_topic", "/joy")
        self.declare_parameter("max_vx", 0.10)
        self.declare_parameter("max_yaw_rate", 0.30)
        self.declare_parameter("axes_bias", 0.0013)
        self.declare_parameter("move_axis", 0)
        self.declare_parameter("turn_axis", 1)
        self.declare_parameter("pitch_axis", 2)
        self.declare_parameter("roll_axis", 3)
        self.declare_parameter("stand_up_button", 4)
        self.declare_parameter("height_switch_button", 5)
        self.declare_parameter("jump_button", 6)
        self.declare_parameter("speed_button", 7)

        self.tita_ns = str(self.get_parameter("tita_ns").value).strip("/") or "tita"
        self.joy_topic = str(self.get_parameter("joy_topic").value)
        self.max_vx = float(self.get_parameter("max_vx").value)
        self.max_yaw_rate = float(self.get_parameter("max_yaw_rate").value)
        self.axes_bias = abs(float(self.get_parameter("axes_bias").value))
        self.move_axis = int(self.get_parameter("move_axis").value)
        self.turn_axis = int(self.get_parameter("turn_axis").value)
        self.pitch_axis = int(self.get_parameter("pitch_axis").value)
        self.roll_axis = int(self.get_parameter("roll_axis").value)
        self.stand_up_button = int(self.get_parameter("stand_up_button").value)
        self.height_switch_button = int(self.get_parameter("height_switch_button").value)
        self.jump_button = int(self.get_parameter("jump_button").value)
        self.speed_button = int(self.get_parameter("speed_button").value)

        self.cmd_twist_topic = f"/{self.tita_ns}/command/manager/cmd_twist"
        self.cmd_pose_topic = f"/{self.tita_ns}/command/manager/cmd_pose"
        self.cmd_key_topic = f"/{self.tita_ns}/command/manager/cmd_key"

        self.twist_pub = self.create_publisher(Twist, self.cmd_twist_topic, 10)
        self.pose_pub = self.create_publisher(PoseStamped, self.cmd_pose_topic, 10)
        self.key_pub = self.create_publisher(String, self.cmd_key_topic, 10)
        self.last_buttons: list[int] = []
        self.height_toggle = False
        self.create_subscription(Joy, self.joy_topic, self._joy_cb, 10)

        self.get_logger().info(
            f"Listening on {self.joy_topic}; publishing manual topics "
            f"{self.cmd_twist_topic}, {self.cmd_pose_topic}, {self.cmd_key_topic}"
        )

    def _axis(self, axes: list[float], index: int) -> float:
        if index < 0 or index >= len(axes):
            return 0.0
        value = float(axes[index])
        return 0.0 if abs(value) < self.axes_bias else value

    def _button(self, buttons: list[int], index: int) -> int:
        if index < 0 or index >= len(buttons):
            return 0
        return int(buttons[index])

    def _publish_key(self, value: str) -> None:
        self.key_pub.publish(String(data=value))

    def _publish_pose(self, pitch_axis: float, roll_axis: float) -> None:
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = "base_link"
        pose.pose.position.x = 0.0
        pose.pose.position.y = 0.0
        pose.pose.position.z = 0.0 if not self.height_toggle else 0.05
        roll = float(roll_axis) * 0.30
        pitch = float(pitch_axis) * 0.30
        w, x, y, z = _quat_from_rpy(roll, pitch, 0.0)
        pose.pose.orientation.w = w
        pose.pose.orientation.x = x
        pose.pose.orientation.y = y
        pose.pose.orientation.z = z
        self.pose_pub.publish(pose)

    def _joy_cb(self, msg: Joy) -> None:
        axes = list(msg.axes)
        buttons = list(msg.buttons)

        twist = Twist()
        twist.linear.x = self._axis(axes, self.move_axis) * self.max_vx
        twist.angular.z = self._axis(axes, self.turn_axis) * self.max_yaw_rate
        self.twist_pub.publish(twist)

        pitch_axis = self._axis(axes, self.pitch_axis)
        roll_axis = self._axis(axes, self.roll_axis)
        self._publish_pose(pitch_axis, roll_axis)

        current_buttons = [self._button(buttons, i) for i in range(max(
            self.stand_up_button,
            self.height_switch_button,
            self.jump_button,
            self.speed_button,
        ) + 1)]
        if not self.last_buttons:
            self.last_buttons = [0] * len(current_buttons)

        def rising_edge(index: int) -> bool:
            return self._button(current_buttons, index) == 1 and self._button(self.last_buttons, index) == 0

        if rising_edge(self.stand_up_button):
            self._publish_key("transform_up")
        if rising_edge(self.height_switch_button):
            self.height_toggle = not self.height_toggle
            self._publish_key("transform_down")
        if rising_edge(self.jump_button):
            self._publish_key("jump")
        if rising_edge(self.speed_button):
            self._publish_key("balance")

        self.last_buttons = current_buttons


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = TitaJoyBridgeNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
