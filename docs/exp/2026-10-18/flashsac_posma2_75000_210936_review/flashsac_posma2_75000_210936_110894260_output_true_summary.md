# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-18T21:09:36+09:00
- Host: tita
- ROS distribution: humble
- Namespace: tita4252763
- Output enabled: true
- Leg action filter: ma2_legs (50 Hz update; wheels pass through; raw last_action)
- Leg notch: 8.3 Hz, Q 3.0 (active only for ma2_notch_legs; hardware effect NOT_TESTED)
- Velocity bias enabled: false
- Velocity bias limit: additional torque +/-0.8 Nm per wheel (converted using wheel Kd and radius)
- Velocity bias response sign: 1.0 (hardware sign NOT_TESTED)
- Velocity bias acquisition: ignore 0-1 s, estimate 1-3 s, correction OFF until 3 s (each neutral hold)
- Velocity bias application: no torque seed; 1 s ramp; correction slew <=0.8 Nm/s per wheel; tracking anti-windup
- Velocity bias posture guard: 5 deg pitch deviation from acquisition mean; latch OFF until command exit/reentry or RL reset
- Supporting sit: 4 s; full leg PD, nominal encoder/IMU CoM wheel balance; software stop latched
- Final torque limits: policy config per-motor effort limits
- Existing service: tita-bringup.service (automatic stop; never automatic restart)
- Policy bundle: flashsac_posma2_75000
- Policy checkpoint SHA256: 9c22f34e0e3b9d7840f29250c214452bb84cadde6037d277d90df55221e84150
- Console: flashsac_posma2_75000_210936_110894260_output_true_console.log
- Bag: flashsac_posma2_75000_210936_110894260_output_true_bag
- Bag console: flashsac_posma2_75000_210936_110894260_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: ma2_legs

## Installed policy file SHA256

```text
128734f230868b947c9eac59ef647b8394043c6603781a335fd4e3b4700a2001  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_posma2_75000/policy.onnx
45a2e773f5ccf43b770829184b22537a6de1ce8da092727264446ac32287c28a  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_posma2_75000/config.json
```
a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
b837bb81aee2fe0de2c4e20401d81e2852e4dafe2b490a6a2ac27151df4f3208  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 7204
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 7225

- Finished: 2026-10-18T21:11:24+09:00
- Runner exit code: 130
