# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-18T20:24:50+09:00
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
- Policy bundle: flashsac_posma2_50000
- Policy checkpoint SHA256: baba6974b76d4e8a7b7107cdfab9d2b7bb73695df00419009279549ebd51f992
- Console: flashsac_posma2_50000_202450_389656744_output_true_console.log
- Bag: flashsac_posma2_50000_202450_389656744_output_true_bag
- Bag console: flashsac_posma2_50000_202450_389656744_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Action filter sample: /sim2real/action_filter_sample (same IDs/time; filter mode and applied action; teacher uses applied targets)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

- Resolved leg action filter: ma2_legs

## Installed policy file SHA256

```text
4b922a52b4e371f4e1ed28d64a0a9d4211161ba24950a1d5a92d2ccf26918553  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_posma2_50000/policy.onnx
2b11c12bf531b8fd92558d3b36e04f49aa91fcae7b97f187413b127780bb93be  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_posma2_50000/config.json
```
a5c3e897f7d73408a8695f4c2dc77b6e28768efb55ad62c364aa2deee0ebde76  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
369f0dacce9db1089822ac2798273d4f9acc9e74cb98e8a4974e7ffc87eb4502  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 17563
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 17610

- Finished: 2026-10-18T20:26:58+09:00
- Runner exit code: 130
