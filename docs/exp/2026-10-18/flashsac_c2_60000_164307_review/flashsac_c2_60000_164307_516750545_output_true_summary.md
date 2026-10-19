# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-18T16:43:07+09:00
- Host: tita
- ROS distribution: humble
- Namespace: tita4252763
- Output enabled: true
- Leg action filter: none (50 Hz update; wheels pass through; raw last_action)
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
- Policy bundle: flashsac_c2_60000
- Policy checkpoint SHA256: b4c8ae072787c3119864e75c2ebfbaf8284a02976dc68f1f282ad9480ae2e116
- Console: flashsac_c2_60000_164307_516750545_output_true_console.log
- Bag: flashsac_c2_60000_164307_516750545_output_true_bag
- Bag console: flashsac_c2_60000_164307_516750545_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

## Installed policy file SHA256

```text
b12e40267bb3247762b0dd6283bd9f9cafffac52597ca74b387790bb4e925b7f  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_c2_60000/policy.onnx
9561fd1a7d9e5f75a1a9916e0c32d4a705109c4795dac9636fbac0ad877ffde1  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_c2_60000/config.json
```
80c912f103b109868bb6dd50c26404f5144bdff089c5be09a374a145b2672fc8  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
bb441f7c829c5e1e7c5172bb8825b87ff0efc0e176162cd506bd07612605b309  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: inactive
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 111535
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 111556

- Finished: 2026-10-18T16:44:38+09:00
- Runner exit code: 130
