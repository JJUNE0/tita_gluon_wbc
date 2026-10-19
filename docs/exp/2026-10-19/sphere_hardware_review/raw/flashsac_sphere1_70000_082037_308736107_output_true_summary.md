# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-19T08:20:37+09:00
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
- Policy bundle: flashsac_sphere1_70000
- Policy checkpoint SHA256: 8e23cf5d1844a6d825482939e5cfc455cd672dd566b2320570080ff606782c77
- Console: flashsac_sphere1_70000_082037_308736107_output_true_console.log
- Bag: flashsac_sphere1_70000_082037_308736107_output_true_bag
- Bag console: flashsac_sphere1_70000_082037_308736107_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: ma2_legs

## Installed policy file SHA256

```text
df54bb61b09c681aad403b41ae52dc83807002f2832b8f969c2ba56a441297d7  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere1_70000/policy.onnx
892bf68e509ad088d0ba6c172042bd8433dedefac3fd0c3294fd58be095a3c65  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_sphere1_70000/config.json
```
a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
d4c3539717efd649a35c1f358571f16da3ea6421abb873c5db5832bacca18449  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: inactive
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 12925
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 12946

- Finished: 2026-10-19T08:21:32+09:00
- Runner exit code: 130
