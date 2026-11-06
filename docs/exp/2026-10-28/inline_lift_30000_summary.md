# Inline 30k physical foot-lift evaluation and contact-sign fix

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: FAIL for learned physical foot lift in model_30000; PASS for
native/production sim2sim trace execution and saved gait/action support; PASS
for the contact-sign correction regression. Corrected-policy performance is
NOT_TESTED because retraining has not started at this inspection.

Policy Checkpoint SHA256: `5911e49063c8ad402394c0d3b59f490a391fc8b6275c7c9dcbb4cc410bfdbad4`.
ONNX SHA256: `72654219bde8c2cd8291de21dc7c795a757f0daeb0b22edbe23f36c8d52b6978`.
Checkpoint: `mj_lab/logs/flash_sac/tita_mjlab_105509_377182/model_30000`.
Branch: `agent/codex/tita-walk`. No commit, push, PR or robot operation.

## Main result

The gait observation is enabled during forward/back commands and disabled at
zero/turn commands. The physical robot still drives on both wheels. Foot lift
above 1 cm, combined with wheel contact below 5 N, was observed **zero times**
in all four conditions in both backends.

| Forward vx=0.5 m/s | Native mjlab | Production sim2sim |
|---|---:|---:|
| Left maximum wheel clearance | 1.514 mm | 0.153 mm |
| Right maximum wheel clearance | 0.781 mm | 0.116 mm |
| Desired-swing samples with >1 cm clearance and no contact | 0% / 0% | 0% / 0% |
| Complete lift intervals | 0 / 0 | 0 / 0 |
| Mean actual vx | 0.585 m/s | 0.637 m/s |

The 4 cm height target and 0.4 s swing have therefore not emerged physically
in this checkpoint. This is a mid-training result, not a prediction of the
final policy. Native forward/back cases had no terminations; one native turn
case terminated/reset. All four sim2sim cases survived their 12-second runs
without base/knee ground-contact failure or excessive tilt.

Native evaluation used 16 environments (four per condition), the saved noise
and full domain randomization, fixed commands and seed 42. Conditions were
zero, vx=+0.5, vx=-0.5 and yaw=+0.5. Metrics exclude the first two seconds of
an episode and terminal/reset samples. Sim2sim used the production ROS node,
its posture startup, nominal saved PD/contact configuration and the same four
commands for 12 seconds each after RL entry. These are different physical and
randomization conditions; their height differences are not presented as a
controlled numerical backend equivalence test.

Physical lift requires both height >1 cm and contact-force magnitude <=5 N.
A sensor sign check corrected the evaluator's initial signed-z assumption;
final native traces include signed force z and force magnitude for inspection.
Native supports both wheels nearly continuously, not flight.

![Desired vs measured clearance](inline_lift_30000_clearance.png)

Native trace/result: `inline_lift_30000_native.npz`, `.json`, `.log`.
Sim2sim trace/result: `inline_lift_30000_sim2sim.npz`, `.json`, `.log`.
Actual sim2sim video: `inline_lift_30000_sim2sim_forward.mp4`.
Existing native W&B preview: `tita_mjlab_105509_377182_videos/model_30000.mp4`.

## Contact-reward implementation defect

The existing native reward used:

```python
actual = env.scene["feet"].data.force[:, :, 2] > 5
```

mjlab's contact wrench has primary-to-secondary orientation; in the measured
supported poses, signed z is approximately **-128 to -132 N per wheel**, with
force magnitude approximately 133 N. The old predicate marked these supports
as no contact. Across 4,008 valid gait samples, the signed-positive predicate
reported 0% contact, while magnitude reported 99.663% contact. The old raw
contact-schedule reward averaged 0.0653; applying the corrected predicate to
the same samples gives 0.6500. These are diagnostic recalculations, not results
of a newly trained policy.

The implementation has been corrected to:

```python
actual = env.scene["feet"].data.force.norm(dim=-1) > 5
```

This makes contact detection independent of wrench sign. Existing base/knee
termination already used magnitude and is unchanged. Reward weight, clearance,
command sampling, gait timing and wheel actions were not changed in this task.
The defect is a concrete reason the intended contact-schedule learning signal
was ineffective; other reward tradeoffs may still limit lifting after correction.

Regression covers positive/negative supported forces, a correctly lifted foot,
both unsupported feet, and gait-disabled masking. Native suites passed
**29 tests / 8 task-specific skips**; `inline_lift_contact_regression.log`.
`./scripts/agent-check.sh` also passed; `inline_lift_agent_check.log`.

## sim2sim support

The existing runtime already restores:

- Full gait cycle 2 s / frequency 0.5 Hz; stance ratio 0.8; left/right offset 1 s.
- Five saved gait observations and straight-only activation.
- Gait disabled for zero/yaw commands.
- Both wheel velocity actions enabled throughout gait, from saved `gate=always`.

The trained actor determines physical leg motion. No playback leg trajectory
or forced lifting was inserted. The 30k checkpoint exported successfully with
256 parity samples, maximum absolute error `4.5299530029296875e-06`;
`inline_lift_30000_prepare.log`. Thus the measured lack of lifting appears in
both native training playback and the production sim2sim implementation.

Run from the repository root:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py \
  --ckpt mj_lab/logs/flash_sac/tita_mjlab_105509_377182/model_30000
```

Press 1, wait for sit, then 0. Hold w/s for straight forward/back commands;
a/d for yaw; r requests zero velocity. These keys are read from the terminal.

## Training state and review

At this inspection the original inline trainer remains alive, PID 1108441,
latest recorded step 41,100 / 100,000. It retains the previously imported
reward implementation. The correction on disk does not hot-reload into that
running Python process. The user has been asked whether to stop this run and
restart from scratch with the correction; no restart was performed yet.

The pre-fix loaded source snapshot SHA256 is
`abb7143ecf51bdecc0a18bcffcec0d3cdb8741d40ef00452229f31c8fb1b9be3`. Corrected on-disk source SHA256:
`e17190482dbf039320ac6f9e33f2d3fc33880eac6f5bce268a8a26cdf34a6203`. Checkpoint disk-source hashes
saved after this edit can reflect the corrected file while the old process
still executes its imported code. The startup launch record and pre-fix snapshot
preserve the actual old implementation for provenance. Evaluation inference
uses frozen actor weights; the reward-only correction does not change them.

Changed files:

- `mj_lab/robots/tita/mdp.py`: sign-independent native contact reward.
- `test/test_mjlab_inline.py`: regression for real contact-force orientation.
- New `test/evaluate_inline_foot_lift.py`: physical height/contact measurements,
  native and production sim2sim evaluation, and sim2sim forward video.
- This report and supporting evidence under `docs/exp/2026-10-28/`.

Starting status: `inline_lift_preexisting_status.txt`; correction diff:
`inline_lift_reward_fix.diff`; pre-fix snapshots: `inline_lift_before_*`.
Final task diffs were inspected; pre-existing dirty edits/staged renames and
unrelated files were preserved. Sim2sim production sources were not modified.
Remaining work requiring a separate experiment is training a corrected policy
from scratch and repeating the same physical foot-lift evaluation.
