# ROS 2 Humble deployment

## Source layout

The repository mirrors the two workspaces used on the TITA SBC:

```text
direct_ws/src/ddt_ros2_control
direct_ws/src/tita_stage1_controller
lowlevel_ws/src/tita_low_level_sdk
```

Run `scripts/bootstrap_upstream.bash` once to fetch the pinned upstream and apply the overlay.

## Desktop or CI build

```bash
source /opt/ros/humble/setup.bash
./scripts/build_humble.bash
```

The C++ controller downloads a SHA256-pinned ONNX Runtime 1.19.2 binary archive for the current
CPU architecture during the first build.

## SBC sync

Back up the target packages first. Synchronize only these source trees; never synchronize build,
install, log, runtime-ledger, policy, or run-data directories. Preserve the expected SBC layout
under `/home/robot/direct_ws` and `/home/robot/lowlevel_ws` unless all absolute configuration paths
are deliberately reviewed.

After synchronization:

```text
1. compare source SHA256
2. clean only the selected package build/install directories
3. package-select build and test
4. inspect plugin prefixes and ldd
5. run command-free preflight with vendor service active
6. confirm command output remains DISABLED
```

Deployment is not authorization for Direct mode. Do not stop the service or open the real
HardwareBridge during source deployment.

## Expected external files

```text
/home/robot/tita_policy/policy.onnx
/home/robot/direct_ws/src/ddt_ros2_control/start.bash
```

The policy is intentionally excluded from Git. Its expected SHA256 is documented in README.

