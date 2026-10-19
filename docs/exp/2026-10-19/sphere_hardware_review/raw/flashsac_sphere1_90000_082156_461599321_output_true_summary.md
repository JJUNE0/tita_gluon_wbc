# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-19T08:21:56+09:00
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
- Policy bundle: flashsac_sphere1_90000
- Policy checkpoint SHA256: df2a03faeb6e054310c8cc0c2c11f811c1f6e845dd87a66c40ff3cd29dd8b311
- Console: flashsac_sphere1_90000_082156_461599321_output_true_console.log
- Bag: flashsac_sphere1_90000_082156_461599321_output_true_bag
- Bag console: flashsac_sphere1_90000_082156_461599321_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: ma2_legs

## Installed policy file SHA256

```text
08d57aa5b0d63063ddcd1f64a08fc545f7ad2ab317aa1c1044cb80ea15a0710a  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere1_90000/policy.onnx
cfd82318fced4143654bff6e9071d1cba312d0203ffcecca549ddecdf6e55479  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere1_90000/config.json
```
a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
d4c3539717efd649a35c1f358571f16da3ea6421abb873c5db5832bacca18449  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: inactive
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 13454
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 13479

- Finished: 2026-10-19T08:23:57+09:00
- Runner exit code: 130
