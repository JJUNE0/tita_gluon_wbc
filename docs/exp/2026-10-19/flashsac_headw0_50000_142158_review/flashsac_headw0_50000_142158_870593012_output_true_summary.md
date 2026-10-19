# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-19T14:21:58+09:00
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
- Policy bundle: flashsac_headw0_50000
- Policy checkpoint SHA256: 0a6f8ef2bb8a324bf6f6fb7689297f9001bd4b57896daa0cb9ead4953162f4a7
- Console: flashsac_headw0_50000_142158_870593012_output_true_console.log
- Bag: flashsac_headw0_50000_142158_870593012_output_true_bag
- Bag console: flashsac_headw0_50000_142158_870593012_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: none

## Installed policy file SHA256

```text
284b4166297fafe5606e58d7b66d9e4570980b839ebde433cbd7a85549313a4c  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_headw0_50000/policy.onnx
804d2ab9f0fdb80232706a9dc99f4daacad4b2c0f194c914f99b1d8fd1b7c428  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_headw0_50000/config.json
```
da28fb15980655c5ff73d8db0b094508fdd4382d65af8107c4e2164ff4b21bc3  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
1127f0b47c3b8cef6417f212064ee8e7fbc4bf6ab03054199c23439a0840c543  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 6678
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 6699

- Finished: 2026-10-19T14:30:19+09:00
- Runner exit code: 130
