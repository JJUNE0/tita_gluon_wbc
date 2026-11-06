# One-leg smoothness and sit/stand checkpoint selection

Execution Domain: VALIDATION_SIM; loss audit: TRAINING_SIM

Evidence Status: SUSPICIOUS (finite execution/export checks PASS; performance has stated limits)

Policy Checkpoint SHA256: per selected checkpoint below; all 61 exports and rollout hashes are in selection.json.

## Selection

| Goal | Checkpoint | Main production-loop measurement |
|---|---|---|
| Left support | `mj_lab/logs/flash_sac/tita_mjlab_155513_268911/model_40000` | target rate 1.359 rad/s RMS; gyro >3Hz 0.595 rad/s; longest support 39.74s |
| Right support | `mj_lab/logs/flash_sac/tita_mjlab_201526_001807/model_20000` | target rate 0.442 rad/s RMS; gyro >3Hz 0.055 rad/s; longest support 39.70s |
| Sit/stand, least drift | `mj_lab/logs/flash_sac/tita_mjlab_013009_483244/model_70000` | 2 stable cycles /32.4s; max XY 16.5cm; end XY 15.0cm |

In the production loop, original left40k remains smoother overall than the new left100k run. New left75k has slightly less >3Hz gyro power at friction0.8 but fails the contact criterion at friction1.2; new left25k is a more robust alternative with more action changes.

One-leg ranking prioritizes sustained support, target/action changes and body vibration. XY displacement does not enter that ranking. Small metrics after a fall are excluded.

## Exact hashes and native evidence

- left: `fe8ca785da4353b79ef0b5af37ca073495b2156fa72395d939c3171bef8d27dd`; ONNX `16cf0606dbe1f695bb6a0e920f22a86011c1ad346f9542bf6aec2519ec782257`.
  Native: 64 saved-DR environments, seed42, first 20s episode only; survival 98.4%; mean single support 19.529s.
- right: `50a94bba0fcc64eb5c4b1802aa3c08fbe36bdd742674558b2695d37eb7ce8b02`; ONNX `0c83807bb1a4ba861f7c94c80dd244d81a7c175d7b83d02d46cb7aaeeaeb1bd1`.
  Native: 64 saved-DR environments, seed42, first 20s episode only; survival 100.0%; mean single support 19.834s.
- height: `cff1f2649068d50334a31fb13ca2f2f5612707484a7c411a61267266519fe1d4`; ONNX `486a6ef8d4ee08bed23652988778d0736d1979b70b087eedad9466ac06202118`.
  Native: 64 saved-DR environments, seed42, first 20s episode only; survival 100.0%; stable physical cycle fraction 100.0%.

## Height performance and limits

Height-only command: vx=vy=wz=roll=pitch=0; 0.335→0.08→0.335m at 0.05m/s, two 16.2s cycles, 2s holds. No reset within the 32.4s trial. Production state-machine entry and configured friction 0.8 were used.

Stable physical completion requires a continuous 0.5s low hold at 0.065–0.095m and subsequent continuous 0.5s high hold at 0.30–0.42m, at each command endpoint, without >30deg roll/pitch. This is separate from exact target-height accuracy.

70k: low hold 0.0789m; returned standing mean 0.3628m vs target0.335m; whole-cycle height MAE 3.81cm. The strict ±2cm endpoint metric records 0 cycles: it overshoots standing height, despite performing the full sit/rise motion. This is not a zero-drift or accurate-height policy.

55k/65k/75k/95k were not selected despite small XY offsets: they do not fully sit in this production-loop trial. 10k is the lower-drift fallback at friction1.2; detailed alternatives are in support_height_selection/selection.json.

## Friction probes

| Goal | mu | Support/cycles | Target rate RMS | Max XY (m) | Contact/tilt failure |
|---|---:|---:|---:|---:|---|
| left | 0.5 | 39.68 | 1.235 | 1.869 | False |
| left | 1.2 | 39.78 | 1.213 | 1.481 | False |
| right | 0.5 | 39.54 | 0.424 | 5.445 | False |
| right | 1.2 | 39.08 | 0.278 | 17.052 | False |
| height | 0.5 | 2 | 0.705 | 0.326 | False |
| height | 1.2 | 2 | 0.704 | 0.474 | False |

## Right actor-loss change near 56k

Source: flash_rl/agents/flashSAC/update.py: actor_loss = mean(alpha*log_pi - min(Q1,Q2)); actor/mean_action = actions.mean() over the replay minibatch and all eight signed action components. It is neither action magnitude nor an action-rate metric.

Saved right reward normalization: at55k G_abs_max=11.5003, variance=5.9574, denominator=2.44079; at60k G_abs_max=21.0711 and denominator=4.21423. normalize_rewards divides by max(sqrt(return_variance+eps), G_abs_max/5). Thus normalized rewards shrink to about57.9% of the preceding scale. The maximum is monotonic and remains21.0711 through100k. Left denominator remains2.36759.

Right loss55k −2.88668 →60k −1.77872, temperature0.00117→0.00070. Reconstructing mean min-Q as −alpha*entropy−actor_loss gives2.891→1.781; multiplying by the saved normalization denominator gives7.057→7.507, much closer in scale. Raw return74.61→72.95 and logged single support19.76→19.30s, recovering to19.78s at100k. The loss begins rising around56.0k and is consistent with a critic/value rescaling transient rather than sustained behavior collapse. No task/curriculum transition is configured there.

The trigger was an unusually large absolute discounted return. Positive per-step reward is bounded by(2+2+0.5)*0.02=0.09, hence positive discounted return ≤9 at gamma0.99;21.0711 must be a negative-return outlier. Which exact transition/penalty produced it cannot be recovered from 5k checkpoints and 100-step aggregate logs; the full replay was not saved. Do not infer a particular physics failure without that trace.

The left/right signed action means need not match: support/swing roles and independently learned compensation change the average. In the saved-noise native55k rollouts (5–20s), the airborne wheel normalized mean is about−0.852 (left-support run, right wheel) versus+0.846 (right-support run, left wheel); support-wheel means are−0.028/+0.046. The opposite airborne-wheel spin is a major contributor to the signed scalar difference. These are rollout statistics, not the exact replay minibatch used by the training metric. The one-leg reward has no direct wheel-speed/magnitude cost; constant fast airborne-wheel spin can have small action changes. Compare per-joint mean/absolute mean and temporal differences. The later right model has more jitter in actual playback, but actor loss alone does not diagnose that.

## Validation and artifacts

- Native sweep: 20 checkpoints per fresh run plus original left40k; frozen deterministic inference, saved noise/DR and push events, 64 environments, seed42. Startup DR shared within each run; first episodes only, terminal snapshots before wrapper reset.
- Smoothness recommendations prioritize the production sim2sim loop. Native noise/delay/physics randomization changes action-rate rankings; all native values are retained in selection.json. The recommendation is not an assertion that the same checkpoint wins under every disturbance or sensor condition.
- Production: same saved observation/action/PD contract; verified ONNX exports (256 random samples each), zero motion commands, 40s one-leg and32.4s height trials. One-leg smoothness excludes first5s. Additional friction0.5/1.2 probes for finalists.
- Target rate is RMS finite difference of actual clipped leg position targets /0.02s. Action-step L2 uses gain-scaled policy actions, matching the action-rate reward convention. Body vibration is RMS body-frame roll/pitch gyro after removing frequencies below3Hz; slow sway is reported separately.
- Finite probes do not establish hardware readiness. Right20k is much quieter than left40k; left still has visible body sway. Height drifts and overshoots its standing target.
- No training/controller/reward settings changed. New evaluation/report scripts only in test/; outputs in docs/exp/2026-11-01/.

Changed files: `test/select_support_height_checkpoints.py` (native frozen sweep), `test/sweep_support_height_sim2sim.py` (production-loop smoothness/friction/video probes), `test/report_support_height_selection.py` (loss audit and plots), and this report/evidence directory.

Checks: `./scripts/agent-check.sh`; see `support_height_agent_check.log` for actual results. Trace/hash/video consistency is recorded in `support_height_selection/artifact_checks.json`.

Branch: `agent/codex/tita-walk`

Graphs: `one_leg_smoothness.png`, `height_cycle_drift.png`, `loss_action_audit.png`. Videos: `left_selected.mp4`, `right_selected.mp4`, `height_selected.mp4`.

## Interactive sim2sim commands

Run from the repository root. Press1, wait for SIT, then0 to enter the policy. These are independent fixed-side policies; they have no support-mode command.

left:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt mj_lab/logs/flash_sac/tita_mjlab_155513_268911/model_40000
```

right:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt mj_lab/logs/flash_sac/tita_mjlab_201526_001807/model_20000
```

height:

```bash
python3 sim2sim/sim2sim_ros2_jazzy/launch/sim2sim.launch.py --ckpt mj_lab/logs/flash_sac/tita_mjlab_013009_483244/model_70000
```

For height: `o` lowers the target1cm, `u` raises1cm, `p` returns to0.335m. The saved ramp is5cm/s and bounds are0.08–0.335m. The evaluation video supplies the full two-cycle trajectory automatically; the interactive launcher accepts manual height commands.
