# Validation & launch commands

Environment: Python venv `~/venvs/cosim_ros2_jazzy`, ROS2 Jazzy. The colcon
workspace root for this package is `tita_gluon_wbc/sim2sim/` (NOT `tita_gluon_ws/` —
`build/`, `install/`, `log/` all live under `sim2sim/`).

## 1. Export ONNX from a new checkpoint (training repo side)

```bash
cd /home/cocel/Desktop/Research/isaaclab_add_reward_autotuning
python scripts/co_rl/play.py \
  --task <CORRECT_REGISTERED_TASK_ID> \
  --algo mooppo --num_policy_stacks 1 --checkpoint <model_N.pt> \
  --num_envs 1 --headless
```
- Find the correct task ID by grepping the relevant `tita_env/__init__.py` /
  `params/agent.yaml` for the run — do not assume it matches the previous
  checkpoint's task ID (see `01_checkpoint_history.md` gotchas).
- `play.py` keeps running an infinite render loop after export completes — kill it:
  ```bash
  ps aux | grep "[c]o_rl/play.py" | awk '{print $2}' | xargs -r kill -9
  ```
- For an RMATeacher-style two-network checkpoint, the encoder needs a separate
  pure-torch export script (load `encoder.*` state_dict keys into a standalone
  `Encoder` module, `torch.onnx.export`) since `play.py` only exports the combined
  actor graph — see `02_rma_teacher_architecture.md`.
- Copy/verify the exported `.onnx` into `tita_gluon_wbc/tita_gluon_ws/deploy/tita/`
  with a descriptive, checkpoint-specific filename (never overwrite a prior export).
  Record its SHA256 in the config file's comment block.

## 2. Create/copy the config file

```bash
cd sim2sim/cosim_ros2_jazzy/config
cp <most_similar_prior_config>.yaml tita_moo_stand_drive_<date>_<iter>_<tag>.yaml
```
Then edit: `policy.path` (and `policy.rma_encoder_path` etc. if RMA),
`policy.height_norm_center`/`height_norm_half_range` (re-derive per checkpoint, do
not blindly carry forward), `command.default_height_m`, and the header comment block
(provenance: run id, checkpoint SHA256, ONNX SHA256, what changed vs. the previous
checkpoint). Leave `reference_transform_up.stand_jpos` alone unless the user
explicitly asks to change it (see `04_reference_transform_up_issue.md`).

## 3. Rebuild the ROS2 package (only needed for brand-new files)

```bash
source ~/venvs/cosim_ros2_jazzy/bin/activate
cd /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim
colcon build --symlink-install --paths cosim_ros2_jazzy --packages-select cosim_ros2_jazzy
```
Plain edits to existing `.py` files take effect immediately (symlink-install) and do
NOT require a rebuild. A brand-new `.yaml` config file DOES need this rebuild so it
gets symlinked into `install/cosim_ros2_jazzy/share/cosim_ros2_jazzy/config/`.

## 4. Validate headless before showing the viewer

```bash
source ~/venvs/cosim_ros2_jazzy/bin/activate
source /opt/ros/jazzy/setup.bash
source /home/cocel/Desktop/Research/tita_gluon_wbc/sim2sim/install/setup.bash
CFG="$(ros2 pkg prefix cosim_ros2_jazzy)/share/cosim_ros2_jazzy/config/<new_config>.yaml"
timeout 20 ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  config:="$CFG" viewer:=false keyboard:=false joystick:=false \
  > /home/cocel/Desktop/Research/tita_gluon_wbc/test/eval_logs/<name>_headless.log 2>&1
```
Check the log for: node starting cleanly, correct policy path/SHA256 logged, no
`ValueError`/`RuntimeError`/traceback from ONNX shape validation, process still
alive at the end (no crash).

## 5. Launch the viewer for the user

```bash
CFG="$(ros2 pkg prefix cosim_ros2_jazzy)/share/cosim_ros2_jazzy/config/<new_config>.yaml"
ros2 launch cosim_ros2_jazzy tita_mujoco_sim2sim.launch.py \
  config:="$CFG" viewer:=true keyboard:=true joystick:=false
```
**Gotcha**: `keyboard_command_node` opens `/dev/tty` directly and will crash with
`OSError: [Errno 6] No such device or address: '/dev/tty'` if the whole launch is
backgrounded via `nohup ... &` from an agent shell (no controlling TTY). If
launching from an automated/background shell:
- Launch with `keyboard:=false` and let the user run
  `ros2 run cosim_ros2_jazzy keyboard_command_node --ros-args -p tita_ns:=tita`
  themselves in their own interactive terminal — it connects over the same ROS
  topics regardless of which process started the sim node, as long as `tita_ns`
  matches.
- Watch for duplicate sim/viewer processes if a first background-launch attempt
  silently half-succeeded (check `pgrep -af "mujoco_policy_node|tita_mujoco_sim2sim"`
  before relaunching, kill stragglers first).

## Useful smoke-test scripts

`test/tita_sensor_readonly_probe.py` and `test/test_tita_gluon_moo_smoke.py` exist
under `/test/` per the repo's debugging/test-code policy (`AGENTS.md` §5). Earlier
summaries in this line of work referenced `moo_handoff_probe.py`/`moo_diag_probe.py`
— **these do not currently exist in `/test/`**; the actual validation pattern used
was `diagnostic:=true` headless launches (see `test/eval_logs/moo_launch_*_diag.log`
for examples) plus the headless smoke-test above. If a handoff-specific probe script
is needed, write it fresh under `/test/`, don't assume the old one still exists.
