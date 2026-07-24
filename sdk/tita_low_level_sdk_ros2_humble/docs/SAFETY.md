# Safety and operator gates

## Default state

The launch defaults are inert:

```yaml
execute_vendor_stop: false
execute_start_bash: false
enable_hardware_output: false
operator_arm: false
auto_enter_rl: false
respawn: false
```

An operator-arm service is a separate runtime transition. Starting a launch with permissive
arguments does not arm the robot.

## Forbidden without fresh approval

- stopping, starting, or restarting the vendor service
- invoking the official `start.bash`
- transmitting raw CAN/CAN-FD frames
- changing motion-board mode
- activating the real ros2_control hardware component
- loading or switching a real command-producing controller
- writing motor commands or enabling RL output

Historical approval does not apply to a new full-power session.

## Preconditions for a real takeover

- full TITA power session established
- vendor service active and exact vendor FSM `idle`
- eight vendor motors reported Online before takeover
- policy/config/controller/logger hashes verified
- robot physically supported
- immediate approved power cut available
- operator understands that graceful Direct-to-MCU rollback is unconfirmed

After approval, the supervisor must stop only `tita-bringup.service`; broad `pkill` and `killall`
are prohibited. It then proves all vendor writers are gone before the official script executes.

## Official Direct request

Only the exact pinned upstream `ddt_ros2_control/start.bash` is permitted. Its raw CAN sequence
must not be copied into Python, C++, another shell script, documentation, or an operator alias.
Exit code zero alone is not confirmation; the stack uses composite bridge/controller/feedback
evidence validated in the real Stage 1 test.

## Watchdogs

Every real command cycle checks sensor freshness, finite state/action/target, ownership,
interface correlation, body attitude, angular velocity, joint envelope, control deadline, motor
feedback, write success, clipping, and logger correlation. Critical failures block new RL output
and enter SAFE_HOLD rather than holding the last policy action.

## Confirmed recovery

```text
SAFE_HOLD active
-> robot physically supported
-> operator removes full TITA power
-> operator restores full TITA power
-> vendor stack boots in MCU mode
-> exact FSM idle is re-verified
-> no stale Direct process remains
```

The software must not automate this process or restart the vendor stack while the motion board may
still be in Direct mode.

## Current limitation

The most recent gain-0.3 Stage 3 run showed a persistent approximately 6 Hz pitch/L1/R1
closed-loop oscillation and eventually crossed the retained `2.5 rad/s` angular-velocity watchdog
during combined `vx=-0.3, yaw=-0.3`. This stack is not approved for unrestricted locomotion.

