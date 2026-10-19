# Frozen FlashSAC run

- Execution Domain: ROBOT_STATE_CHANGING
- Evidence Status: NOT_TESTED (operator must assess motion and telemetry)
- Started: 2026-10-17T13:33:38+09:00
- Host: tita
- ROS distribution: humble
- Namespace: tita4252763
- Output enabled: true
- Velocity bias enabled: true
- Velocity bias limit: +/-2 m/s (no separate correction torque cap)
- Velocity bias response sign: 1.0 (hardware sign NOT_TESTED)
- Velocity bias acquisition: 2 s zero-command hold; bias slew 3 m/s^2
- Final torque limits: policy config per-motor effort limits
- Existing service: tita-bringup.service (automatic stop; never automatic restart)
- Policy checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05
- Console: flashsac_60000_133338_353802215_output_true_console.log
- Bag: flashsac_60000_133338_353802215_output_true_bag
- Bag console: flashsac_60000_133338_353802215_output_true_bag_console.log
- ROS logs: ros/
- Torque topic contains computed command, not measured torque.
- Training sample: /sim2real/training_sample (ROS timestamp, sequence, steady time, raw action, teacher action, bias and output flags)

## Installed policy file SHA256

```text
f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_60000/policy.onnx
d429ad9e60c25137d4bb5e2f26cb50a469fbcecf3a28af0076918a49eb7c035d  /home/robot/tita_ws/install/tita_controller/share/tita_controller/policies/flashsac_60000/config.json
```
d93fd9b078351ac99ddfb8b6b1196486221fa8144b2735ea654b7ca6113e326a  /home/robot/tita_ws/install/tita_controller/share/tita_controller/config/velocity_bias_geometry.json
033811f58fba4a229e0dc7ae7d024d05ad39430553794c491d031fde7c69f148  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/tita_node
6a6616f18f3c067272c7c3ddfdd12d947685cf24b04af2a04599779285204b32  /home/robot/tita_ws/install/tita_controller/lib/tita_controller/run_flashsac.sh

- Previous bringup state: active
- Bringup after stop: inactive/failed/unknown (not restarted on exit)

- Recorder process group: 87554
- MCU Ready request: transport accepted (no independent mode ACK).
- MCU Direct request: transport accepted (no independent mode ACK).
- Controller process group: 87579

- Finished: 2026-10-17T13:34:45+09:00
- Runner exit code: 130
