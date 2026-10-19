# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-19T08:19:20+09:00
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
- Policy bundle: flashsac_sphere2_60000
- Policy checkpoint SHA256: a4c2bfbf6a58240a6623ee8bb8d863774b9336f62df7de3d1993b76725334b2a
- Console: flashsac_sphere2_60000_081920_534970468_output_true_console.log
- Bag: flashsac_sphere2_60000_081920_534970468_output_true_bag
- Bag console: flashsac_sphere2_60000_081920_534970468_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: none

## Installed policy file SHA256

```text
b744091bb984f3540ec9517f4d3a8a70b5d76cf0f1c7a811d122baac15017040  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere2_60000/policy.onnx
7c0b597a7750ec63ae2182edad9af67de616fe069d4630e1810b8e129d4e4c06  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere2_60000/config.json
```
a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
d4c3539717efd649a35c1f358571f16da3ea6421abb873c5db5832bacca18449  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 12380
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 12401

- Finished: 2026-10-19T08:20:19+09:00
- Runner exit code: 130
