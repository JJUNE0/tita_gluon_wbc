# One-command FlashSAC MuJoCo playback

Execution Domain: VALIDATION_SIM; regression/source checks: DESKTOP_DRY_RUN.

Evidence Status: PASS for checkpoint selection, export reuse/automatic export, native headless playback, viewer startup/local keyboard dispatch and clean shutdown. Policy locomotion quality: NOT_TESTED by this launcher integration task. Interactive runtime summaries label deliberate operator interruption SUSPICIOUS rather than implying a completed quality evaluation.

Policy Checkpoint SHA256 (model_15000/actor.pt): `f330e86adeb4b5be2ed276fae01063df63e15bc625d8ad0125746263c42e73a2`.

ONNX SHA256 (15000): `6bff36595e34efefd44879eedab9afb95179da89846df576e56bcc6874ab1d76`.

Policy Checkpoint SHA256 (automatic export, model_20000/actor.pt): `435d9202cb9c11600a670a87ebf3d4c8cd660b7dac497192accac49227a5bb8f`.

ONNX SHA256 (20000): `75832cb21e02e72b84db1dda8012afe778be1166224982583a31c897f1490368`.

Branch: `agent/codex/dev_tita_gluon`.

The user requested a simpler flow than manual environment activation, export, ROS launch and a second keyboard terminal. The new launcher performs those operations from one terminal, reusing the existing simulator and keyboard implementation.

## User command

From the repository root:

```bash
python3 sim2sim/play_flash_sac.py --step 15000
```

Change the step to view another saved checkpoint. Omitting `--step` selects the newest complete checkpoint from the newest run:

```bash
python3 sim2sim/play_flash_sac.py
```

`--run <name-or-path>` selects another training run; `--checkpoint <model_N-directory>` selects an explicit model. The selected absolute path is printed. A missing step in the newest run gives an error listing its available steps; it never silently falls back to an older run that happens to contain that number.

The launcher uses the existing Isaac interpreter for export and the existing MuJoCo interpreter plus ROS Jazzy environment for runtime, without changing the user's shell environment. It verifies checkpoint hashes, automatically exports if necessary and reuses an export only when its manifest/checkpoint/ONNX hashes match. Actor gains remain embedded in ONNX and native MuJoCo scales remain unchanged.

The simulator automatically executes `pose_stand` then `balance`, beginning from the training default pose with RL active. Use `w/s` for forward/backward, `a/d` for yaw, `r` to return velocity commands to zero, and Ctrl-C to close. The existing keyboard slew/idle timeout and simulator command caps remain. No startup keys or second terminal are required.

The launcher uses the existing ROS simulator/keyboard node classes in one process. Keyboard publishers are replaced locally with direct simulator callbacks. The child runtime uses localhost ROS domain 87 and stores ROS logs plus run summaries in `docs/exp/YYYY-MM-DD/`. It does not launch any real-to-sim relay, SDK, robot networking client or physical robot command path.

For finite headless integration checks:

```bash
python3 sim2sim/play_flash_sac.py --step 15000 --headless --steps 50
```

## Changes

- New `sim2sim/play_flash_sac.py`: selection, verified-export cache, environment setup, automatic simulation startup, one-terminal keyboard and cleanup.
- New `test/test_flash_sac_mujoco_launcher.py`: seven regression tests including numeric checkpoint selection/partial saves, no fallback to old runs, cached-export invalidation, literal subprocess arguments, child ROS environment isolation, observation-builder compatibility, local callback dispatch and cleanup after injected failures. The GUI fixture also verifies that an asynchronous viewer thread ends before interpreter teardown.
- Updated `lab/ddt_lab/scripts/flash_sac/README.md`: one-command path placed before lower-level export/ROS instructions.

The existing, pre-edited shared MuJoCo source files remain untouched. The shared node reads two optional MOO observation flags from the plain TITA builder, where they are absent; a local launcher subclass supplies `include_base_height=False` and `include_auxiliary_joint_state=False` for the 33-D TITA actor. Observation contents are unchanged.

## Executed validation and observed behavior

- `python3 sim2sim/play_flash_sac.py --help`: PASS without Isaac/MuJoCo activation.
- Cached model_15000, headless 50 control steps: PASS, native process exit 0; default-pose reset and `rl_0` activation logged. Final base position approximately [−0.0573, 0.0325, 0.4306] m. This is an execution check, not a standstill-quality result.
- Model_20000, no pre-existing export, headless 10 steps: PASS, automatic ONNX export/parity plus native process exit 0. Parity across 256 samples: max absolute difference 4.3511e-6. Startup/selection was recorded for the requested explicit run.
- Native viewer/keyboard using a controlling PTY: graphical initialization, automatic RL activation, terminal key dispatch and Ctrl-C shutdown exercised. The first attempt exited 139 during interpreter teardown. MuJoCo Handle.close only requests asynchronous rendering shutdown; the launcher now waits for the viewer threads. The corrected run exited **0**, logged the locally dispatched `rl_0` key and recorded **viewer_threads_stopped=true**. Its deliberate-stop summary is `tita_flash_sac_mujoco_185248_363469_summary.md`.
- An initial restricted-process attempt reported sandbox interface-enumeration warnings; actual ROS runtime checks were rerun with host access, still restricted to localhost simulation domain 87. No user permission question or hardware action was needed.
- `python -m unittest discover -s test -p 'test_flash_sac*.py' -v`: **48 tests PASS**, including the asynchronous viewer cleanup regression; log `tita_flash_sac_simple_launcher_tests.log`.
- Required `./scripts/agent-check.sh`, final task-relative diff and source-integrity comparison are recorded in `tita_flash_sac_simple_launcher_checks.log`. No unrelated source changes were made.

Native logs: `tita_flash_sac_simple_launcher_native.log`, `tita_flash_sac_simple_launcher_auto_export.log`, `tita_flash_sac_simple_launcher_gui.log` (initial teardown failure), `tita_flash_sac_simple_launcher_gui_checked.log` (corrected exit 0). Runtime JSON/Markdown are saved automatically beside them.

This task simplifies playback and verifies the execution path. It does not evaluate checkpoint-specific tracking, fall probability, standstill drift or sim-to-real performance. The existing MuJoCo/training physics differences remain. Active FlashSAC training settings and PPO environment configs were not modified.
