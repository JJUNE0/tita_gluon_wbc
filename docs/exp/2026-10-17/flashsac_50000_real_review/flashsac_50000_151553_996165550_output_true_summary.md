# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-17T15:15:54+09:00
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
- Policy checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c
- Console: flashsac_50000_151553_996165550_output_true_console.log
- Bag: flashsac_50000_151553_996165550_output_true_bag
- Bag console: flashsac_50000_151553_996165550_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)

## Installed policy file SHA256

```text
0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_50000/policy.onnx
08bf0628ddcfc1bbd964573b56cc64f7b9889476f247098ba5e53b324ed7b6e8  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_50000/config.json
```
fd3f0285acfe42a60bb998e9d3824f4ff669bb326e934c9527e9893f9f26be95  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
efecc46632524e6926d2f7ea14d9c31dd09d60ca293b090639a8e67344d0d861  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: inactive
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 14270
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 14291

- Finished: 2026-10-17T15:17:00+09:00
- Runner exit code: 130
