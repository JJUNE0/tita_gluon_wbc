# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-17T17:38:48+09:00
- Host: tita
- ROS distribution: humble
- Namespace: tita4252763
- Output enabled: true
- Velocity bias enabled: false
- Velocity bias limit: additional torque +/-0.8 Nm per wheel (converted using wheel Kd and radius)
- Velocity bias response sign: 1.0 (hardware sign NOT_TESTED)
- Velocity bias acquisition: ignore 0-1 s, estimate 1-3 s, correction OFF until 3 s (each neutral hold)
- Velocity bias application: no torque seed; 1 s ramp; correction slew <=0.8 Nm/s per wheel; tracking anti-windup
- Velocity bias posture guard: 5 deg pitch deviation from acquisition mean; latch OFF until command exit/reentry or RL reset
- Final torque limits: policy config per-motor effort limits
- Existing service: tita-bringup.service (automatic stop; never automatic restart)
- Policy checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05
- Console: flashsac_60000_173848_866246050_output_true_console.log
- Bag: flashsac_60000_173848_866246050_output_true_bag
- Bag console: flashsac_60000_173848_866246050_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

## Installed policy file SHA256

```text
f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_60000/policy.onnx
d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_60000/config.json
```
f086fa22038124386825752711c83fd20b1ef220cdbad7eaae002463d42b3c73  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
40dbb2566bc13361a8c9cf4e3b3e883243e768980badf851550800e620d8edcf  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 76574
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 76599

- Finished: 2026-10-17T17:39:48+09:00
- Runner exit code: 130
