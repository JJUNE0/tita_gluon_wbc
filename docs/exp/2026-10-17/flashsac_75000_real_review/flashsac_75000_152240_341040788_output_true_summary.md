# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-17T15:22:40+09:00
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
- Policy checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730
- Console: flashsac_75000_152240_341040788_output_true_console.log
- Bag: flashsac_75000_152240_341040788_output_true_bag
- Bag console: flashsac_75000_152240_341040788_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)

## Installed policy file SHA256

```text
2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_75000/policy.onnx
34817048ee7b40836d84de632dff4abfe5b0feb50f3a5f861e951f332450cfae  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_75000/config.json
```
fd3f0285acfe42a60bb998e9d3824f4ff669bb326e934c9527e9893f9f26be95  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
f348d1ac4641c26b3bdd8b19f17d906d24a12568c6112b459980c58f3d0ab044  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: inactive
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 16464
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 16485

- Finished: 2026-10-17T15:23:41+09:00
- Runner exit code: 130
