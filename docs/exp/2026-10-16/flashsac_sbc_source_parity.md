# SBC / PC deployment source parity

- Execution Domain: ROBOT_READ_ONLY / DESKTOP_DRY_RUN
- Evidence Status: PASS
- Date: 2026-10-16 (Asia/Seoul)
- Branch: agent/codex/dev_tita_gluon
- Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05
- ONNX Hash: f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a

Compared all 39 files under src/ (excluding __pycache__), README.md and
run_flashsac.sh between PC sim2real/tita_ws and SBC /home/robot/tita_ws.
The file sets and every SHA256 match. Build/install/log output and docs are not
part of this source comparison; binaries target different PC/SBC architectures.
SBC tita-bringup.service was active with controller PID 941 and joystick PID
1075; no service change or robot execution was performed.
Only this report and its evidence file were added. Physical runtime: NOT_TESTED.

Required `./scripts/agent-check.sh`: FAIL due to pre-existing trailing whitespace
in `lab/ddt_lab/ddt_lab/tasks/manager_based/locomotion/robots/tita/my_flat_env_cfg.py`
at lines 431, 437, 443, 449, 455 and 461. Syntax: PASS (462 files); URDF: PASS
(8 files). Final new-report diff integrity: PASS. Existing runtime files were unchanged.
Log: [flashsac_sbc_source_parity_agent_check.log](flashsac_sbc_source_parity_agent_check.log).

## File SHA256 evidence

```json
{
  "README.md": "ebcad4db94d32b9d7f84e4ee3a3b22ed28d4f4d6618d485cc59ad4610026288e",
  "run_flashsac.sh": "9a2f899855aa8ccde4c651ca3469625f6135173a6fe7f424e50ff8aeba88d62c",
  "src/ros_utils/CMakeLists.txt": "aa02c30ff1da629ce947f4fac12766a4e32d040747ff506fc81a91d701d728e4",
  "src/ros_utils/include/ros_utils/topic_names.hpp": "d55359b230f388d7360a7c7326812d4a6f3d0897dcca8629852e08e21bf15954",
  "src/ros_utils/package.xml": "d61a0c62efba592ee19f2fb9f70e617fd42f46ef7a6ed39712060610cf6e032b",
  "src/teleop_command/CMakeLists.txt": "2c881cbda3a9a4da7ad15e9ffc3d3753b46c8bcea59990909cda79283f0de65c",
  "src/teleop_command/config/param.yaml": "75c3b411f8fa12497f296828d22045ee17cbe5ca0f0a63f85c1eb98bd7d53200",
  "src/teleop_command/include/teleop_command/elrs_emwave_device.hpp": "f5c6188eaf842ea31aa637eb5cf445a39227888fcef2e28e8a2041fc352f5741",
  "src/teleop_command/include/teleop_command/teleop_command_node.hpp": "0ca9477c15245382082e9be46c8bb6403a98989a9eed76673af270079a0a7e1d",
  "src/teleop_command/launch/teleop_command.launch.py": "7c4d774329c8dbff0bd779de9bca30a75bde8cde99b2502264d80760808576eb",
  "src/teleop_command/package.xml": "0494dac080c3aa8c86c7f59217288d8f41b362385a1157bf8f12769d89827d9a",
  "src/teleop_command/src/elrs_emwave_device.cpp": "c8f77fe1b4506e4ee6e395d010eca924541ce7fabec66e3e6c24658b030f2e81",
  "src/teleop_command/src/main.cpp": "5ea97e4135ae2a8bc93f6356fde080a890ee5a70f0bc1c9e3ba4f5bc8abf7b13",
  "src/teleop_command/src/teleop_command_node.cpp": "23e0270997d5d46cece16cb9984543acb4710d7e237152ecfa13aa407cbeaa99",
  "src/teleop_command/src/teleop_command_parameters.yaml": "3dae0ee220a3ec2402b2178d467aae2842b63be3a6bcc8eaa3d96a2b8db8941b",
  "src/tita_controller/CMakeLists.txt": "95c5739290a2e4b122de18f50ae501c3491a781523fe836c5f94c7183b4be30e",
  "src/tita_controller/include/tita_controller/adapter.hpp": "04241f97cc308be3a995b275b1c2edbd31ef942dcc0bbf5fe1515ce4188a6be7",
  "src/tita_controller/include/tita_controller/state_machine.hpp": "06f933bcdf34866f908582ba0fafa052d71042110fad97e9aa33c8d64aad1dfb",
  "src/tita_controller/launch/flashsac.launch.py": "0ef8e3dce321fd87f298de9a34b2220a693eebc1429b86140a39b3787ef24ac0",
  "src/tita_controller/launch/tita.launch.py": "719f8ba860cb7ebd5a2b851c83cf97f61ad3509c4b21cd6d98ab799554d4a999",
  "src/tita_controller/package.xml": "748de52b93e793efd595bf923b44c5d11c81c552731acd81d0ad1e202a453afa",
  "src/tita_controller/policies/flashsac_60000/config.json": "66f6113a3c607839bd79a266716fac856d5b271006d51c7c028230e47f7efe31",
  "src/tita_controller/policies/flashsac_60000/manifest.json": "e1f2d58d729dafedc5fcdde88bd0e83db60897afeea4bc3d266bddbf6fb73fad",
  "src/tita_controller/policies/flashsac_60000/policy.onnx": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "src/tita_controller/src/tita_node.cpp": "f94d103b3bd320a3fe96b8e6addbfba41eed9da55826a5125d3241d8d2d066f9",
  "src/tita_robot/.gitignore": "b57ecbb2de79d85471f152df5342647284021c6b3c2693f257dd501e4d541835",
  "src/tita_robot/CMakeLists.txt": "fa2733db305595b57e535231e39e686ca1c6d95c4eaf86a0c9122efa8fca1b3e",
  "src/tita_robot/include/tita_robot/canfd_api.hpp": "69058650752291a07cff4767a5b7a7cc962cc01e7cd7bec8ed28a0fe06e8aacd",
  "src/tita_robot/include/tita_robot/protocol/can_utils.hpp": "cbcb3346559f50e5e00ee39ebbd5a29f91db8051d635d320d62e3c7dbe50bb1d",
  "src/tita_robot/include/tita_robot/protocol/socket_can_common.hpp": "a916922f3498d29a7231f7fcb17218fda4facd11bd1cb5c26b174858f11ab354",
  "src/tita_robot/include/tita_robot/protocol/socket_can_id.hpp": "f419f551248cb157abda6b59670dbdb06f9d455b2296c6c697bddfdceee3cdf6",
  "src/tita_robot/include/tita_robot/protocol/socket_can_receiver.hpp": "e0bc4b37b8c223456ecaa0819f1d74e82c966e09fef412e8de6ab2168fad0002",
  "src/tita_robot/include/tita_robot/protocol/socket_can_sender.hpp": "9fd7ba2b85686586806c9ac5371cc8dc8a251df9c0de2698ba148a2fe7e000db",
  "src/tita_robot/include/tita_robot/protocol/visibility_control.hpp": "fc9326afb0932bfd2bbbbc61c623ce152adc26c2f9992cd854206a3f062317df",
  "src/tita_robot/include/tita_robot/tita_robot.hpp": "05a044ce22bb69f4abf29c457904f84abbc1ead40a595e981b47725c685e4b31",
  "src/tita_robot/lib/amd64/libtita_robot.so": "16aadb50ebb51e5f9aad96c96048e2fa654b1176c203dc274763b4684c4e8ef5",
  "src/tita_robot/lib/arm64/libtita_robot.so": "22460f0b59fd10265b100ab725828c34a62654f858468f1afaa28359c050ae7d",
  "src/tita_robot/package.xml": "835ba7f4a81598ee41f20d1309cb9a0143f95bd173ee47ad60fd36d5d3a65e1c",
  "src/tita_robot/test/read_write_example.cpp": "b1c01a0ab30a6c9d77a2518a325260f044c5056cfe550b399e4141c2d93d17b8"
}
```
