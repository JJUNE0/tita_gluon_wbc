# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-19T15:37:55+09:00
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
- Policy bundle: flashsac_headw0_65000
- Policy checkpoint SHA256: ff083cbfc8a8571009a27454e75dc88463e9ebc796fa79e8782ccb4a5bea239d
- Console: flashsac_headw0_65000_153755_890122030_output_true_console.log
- Bag: flashsac_headw0_65000_153755_890122030_output_true_bag
- Bag console: flashsac_headw0_65000_153755_890122030_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: none

## Installed policy file SHA256

```text
ede50fde5cc1863758d2c50e70f7902cafb31e2a677c985e0d69b80c2560be0b  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_headw0_65000/policy.onnx
804c94a365ccc4b0d9b3bf08022699d81012ccd251d8606a4646624c88ed1db2  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_headw0_65000/config.json
```
da28fb15980655c5ff73d8db0b094508fdd4382d65af8107c4e2164ff4b21bc3  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
7d514130157b5ee5d77576422342f411c5505b32ac85e10328d50c11033ec2ed  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 10862
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 10883

- Finished: 2026-10-19T15:41:49+09:00
- Runner exit code: 130
