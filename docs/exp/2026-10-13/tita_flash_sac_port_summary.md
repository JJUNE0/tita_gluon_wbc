# TITA My flat environment FlashSAC port

Execution Domains: `DESKTOP_DRY_RUN`, `TRAINING_SIM`.

Evidence Status: `PASS` for CPU learning/integration and repository checks;
`BLOCKED` for native Isaac training because CUDA is unavailable in this process.

Policy Checkpoint SHA256 / ONNX Hash: N/A. No trained TITA checkpoint or ONNX was
produced. CPU fixture checkpoints were synthetic and removed after testing.

Current branch: `agent/codex/dev_tita_gluon`.

## Result and changed files

Added `lab/ddt_lab/scripts/flash_sac/` with `train.py`, `play.py`,
`env_adapter.py`, `runtime.py`, `__init__.py`, `README.md`, and `vendor/`.
The vendor directory contains 17 Python core files, the original MIT license,
and a SHA256 provenance manifest. Added four tests:
`test/test_flash_sac_adapter.py`, `test/test_flash_sac_learning.py`,
`test/test_flash_sac_compile_checkpoint.py`, and
`test/test_flash_sac_entrypoints.py`. Added only this date's evidence artifacts
under `docs/exp/2026-10-13/`.

The default task is `DDT-Velocity-Flat-Tita-My-v0`, resolving the existing
`MyTitaFlatEnvCfg`. Its expected actor/critic/action dimensions are 33/36/8;
actual dimensions are read from native Isaac managers. The actor uses the
existing policy observations; the critic uses its separate privileged group.
The PPO-specific learned velocity estimator and auxiliary loss are absent.
Raw actions are clamped to [-1, 1] before existing native joint/wheel action
transforms. Reward, command, actuator and observation config files are preserved.

The adapter captures terminal observations before Isaac auto-reset and keeps
them separate from the reset observations used by the next policy action.
Source fork patches preserve the critic offset and actual n-step gamma^k
discounts at timeout/termination boundaries. The port also fixes checkpoint
parameter names across compiled/eager execution. Checkpoints save environment
config, weights, optimizer/scheduler/normalizer state, dimensions and hashes;
resume refills replay and starts fresh simulator episodes. Run logs and
summaries are written under `docs/exp/YYYY-MM-DD/`.

## Observed metrics / behavior / log summary

`DESKTOP_DRY_RUN` — `PASS`. Executed:

```bash
PYTHONDONTWRITEBYTECODE=1 TORCHDYNAMO_DISABLE=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  -m unittest discover -s test -p 'test_flash_sac*.py' -v
```

Direct output: `Ran 18 tests in 1.642s`, `OK`, exit 0.
See [CPU test log](tita_flash_sac_cpu_tests.log).
Tests cover true terminal/reset observation separation, independent critic
inputs, action transform preservation, tensor snapshot ownership, finite real
FlashSAC losses and changed weights, checkpoint integrity/optimizer restoration,
parallel n-step timeout/termination discounts, and compiled/eager checkpoint
compatibility. The actual train/resume/play entry points were exercised with
real CPU learners/adapters and mocked Isaac modules: 4 environments for 8 vector
steps with 7 learner updates, resume to step 10 with 2 environments and 1 further
update, then 2 deterministic playback steps. This is CPU integration evidence,
not a physical or native Isaac rollout.

`DESKTOP_DRY_RUN` — `PASS`. Executed the required repository check:

```bash
PYTHONPYCACHEPREFIX=/tmp/tita_flash_sac_agent_check_cache ./scripts/agent-check.sh
```

Direct output: 431 Python syntax checks passed, 0 failed; 13 URDF XML files OK;
diff integrity and experiment directory checks passed; final `PASS`, exit 0.
See [agent-check log](tita_flash_sac_agent_check.log).

`TRAINING_SIM` — `BLOCKED`. Executed the native smoke command:

```bash
PYTHONDONTWRITEBYTECODE=1 TORCHDYNAMO_DISABLE=1 \
  /home/cocel/isaac/env_isaaclab/bin/python \
  lab/ddt_lab/scripts/flash_sac/train.py \
  --task DDT-Velocity-Flat-Tita-My-v0 --num_envs 4 --steps 8 \
  --buffer_size 128 --min_buffer 8 --batch_size 8 \
  --save_every 8 --log_every 1 --logger console --headless
```

Direct output: `RuntimeError: CUDA is unavailable in this process`, exit 1.
The CUDA preflight stopped before AppLauncher or simulation startup.
See [native smoke log](tita_flash_sac_native_smoke.log) and its automatically
generated run summary. Separate read-only checks showed
`torch.cuda.is_available() == False` and `nvidia-smi` could not communicate with
the driver.

`DESKTOP_DRY_RUN` — `PASS`. Both train/play `--help` commands completed using
system Python, without simulator startup. All 18 vendored file entries matched
their recorded source/vendor hashes. The final added-file diff and the three
vendor adaptations were inspected. Thirty pre-existing changed regular files
retained their initial SHA256 values, with no new tracked-file diff introduced.
The target `my_flat_env_cfg.py` SHA256 remains
`01d1423eb91faa9d52512e101affdadff742c27e66124590ee6955d6f27b0b1b`.
See [final added-file diff](tita_flash_sac_final_diff.log).

## Source provenance and remaining limits

Source: local `wolf-quadruped/rl/FlashSAC` fork at
`87edc9061150ae9e962dd84e6544e27a1554b3ab`, including its four pre-existing local
patches. Upstream commit was not available in local tracking refs. Full file
hashes and adaptations are recorded in `vendor/source_manifest.json`; the MIT
license accompanies the code.

Native Isaac compatibility, locomotion quality, CUDA compilation and AMP remain
`NOT_TESTED` beyond the blocked launch preflight. The existing PPO estimator
policy/export interface differs from this FlashSAC actor. FlashSAC ONNX export
and MuJoCo/hardware validation are not implemented in this task. No commit,
push or pull request was created.

GPU smoke/full training/playback/resume commands are in
`lab/ddt_lab/scripts/flash_sac/README.md`.
