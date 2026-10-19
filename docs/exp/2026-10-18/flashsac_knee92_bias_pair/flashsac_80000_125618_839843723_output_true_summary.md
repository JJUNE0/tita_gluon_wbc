# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-18T12:56:18+09:00
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
- Supporting sit: 4 s; full leg PD, nominal encoder/IMU CoM wheel balance; software stop latched
- Final torque limits: policy config per-motor effort limits
- Existing service: tita-bringup.service (automatic stop; never automatic restart)
- Policy checkpoint SHA256: 79f9175bb8c3be0c5138866e30891b90cc1282b6c98023cdb76c2e33b229068c
- Console: flashsac_80000_125618_839843723_output_true_console.log
- Bag: flashsac_80000_125618_839843723_output_true_bag
- Bag console: flashsac_80000_125618_839843723_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)
- Motor feedback: /sim2real/motor_feedback (same sample IDs; SDK-reported Nm, validity, read time and preceding command; not calibrated torque)

## Installed policy file SHA256

```text
26f0d86b65a68475fb8a315fb31e829ae16eaa2cf16dabbbcf38e69f28c933e9  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_80000/policy.onnx
a24c2137969f854fc98cc3027884dbbadad4060f18db7758b028c12ca1405719  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_80000/config.json
```
2e3949c0b445fa328ab33ac7b152d3096170e17e1a863a2a8494fdb79dc0d9ff  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
48e5e2d8db0ca001cc800ad8d15c0e553ec66dfb7b9866ffc8330d77da853c82  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 79657
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 79683

- Finished: 2026-10-18T12:58:16+09:00
- Runner exit code: 130
