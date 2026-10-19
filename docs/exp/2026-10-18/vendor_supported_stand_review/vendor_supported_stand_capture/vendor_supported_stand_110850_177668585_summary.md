# Company baseline, supported standing

- Execution Domain: ROBOT_COMMAND_FREE_RUNTIME
- Evidence Status: NOT_TESTED (capture pending; operator movement/load not controlled)
- Policy checkpoint SHA256: N/A (company controller; FlashSAC is not running)
- Comparison FlashSAC checkpoint SHA256: 79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c
- Started: 2026-10-18T11:08:50+09:00
- Operator annotation: supported standing; wheel load details pending
- Requested capture duration: 60 s CAN; ROS recording overlaps and finalizes afterward
- Capture methods: candump -L receive only; ros2 bag record subscriptions only
- Service/MCU/motor output configuration unchanged
- ROS storage contains only actually published topics; absent topics are not fabricated
- Firmware torque telemetry is not calibrated physical torque

- Capture runtime: PASS (both receive-only processes alive for 60 s)

- Finished: 2026-10-18T11:09:54+09:00
- Capture exit: 0
- Company service after capture: active
