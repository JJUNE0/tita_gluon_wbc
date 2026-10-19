# Company baseline, floor standing / operator joystick commands

- Execution Domain: ROBOT_COMMAND_FREE_RUNTIME
- Evidence Status: NOT_TESTED (capture pending; operator movement/load not controlled)
- Policy checkpoint SHA256: N/A (company controller; FlashSAC is not running)
- Comparison FlashSAC checkpoint SHA256: 79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c
- Started: 2026-10-18T19:27:18+09:00
- Operator annotation: normal floor standing, same support condition as previous RL (corrected by operator)
- Phase: stand_high; commands, if any, are applied by the operator through the existing joystick
- Requested capture duration: 60 s CAN; ROS recording overlaps and finalizes afterward
- Capture methods: candump -L receive only; ros2 bag record subscriptions only
- Service/MCU/motor output configuration unchanged
- ROS storage contains only actually published topics; absent topics are not fabricated
- Firmware torque telemetry is not calibrated physical torque

- Capture runtime: PASS (both receive-only processes alive for $duration s)

- Finished: 2026-10-18T19:28:23+09:00
- Capture exit: 0
- Company service after capture: active
