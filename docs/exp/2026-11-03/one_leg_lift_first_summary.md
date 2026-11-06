# First lift before tight stationary/height shaping

Execution Domains: TRAINING_SIM, VALIDATION_SIM, DESKTOP_DRY_RUN.

Evidence Status: SUSPICIOUS — saved-config comparison, 16 scoped tests, and
short finite learner probes PASS. Both main runs active; learned quality NOT_TESTED.

Policy Checkpoint SHA256, preserved preceding left20k:
`2823a96b297df4a650856bd530c677a510d7cde38ac38072a7acef2ab0e47785`.
Policy Checkpoint SHA256, preserved preceding right20k:
`a9c996e5d6882e681a63491b17f3dff689bbf3c3badd79fed58a759bbf35cc41`.
Main new policy hashes PENDING until scheduled saves. Probe hashes are recorded
in `one_leg_lift_first_config_comparison.json`.

Branch: `agent/codex/tita-walk`.

## Saved baseline versus the unsuccessful stationary-shaping run

The operator asked whether preventing high lifts explains poor learning, then
requested weaker penalties overall and first prioritizing supported lift.
Actual saved20k configurations from reference runs
`tita_mjlab_201526_016988`/`tita_mjlab_201526_001807` and the newer no-cutoff
runs `tita_mjlab_124132_110309`/`tita_mjlab_124132_110350` were compared.

PASS: actions, observations, reset events/DR, scene/model/PD, physics,
terminations, episode length, decimation and agent configuration are exactly
equal on both sides. Base/knee contact failure thresholds are unchanged.
Commands keep the same numeric settings but use an inherited velocity-command
class that additionally stores a fixed support anchor; no new actor observation
was added. Saved actor/critic/action dimensions remain35/39/8.
Evidence: `one_leg_reward_difference_audit.json`, including actual actor hashes.

The significant changes were reward functions and their scales:

| Component | Original reference | Previous stationary shaping |
|---|---|---|
| Lift | Partial progress to4 cm, +2 maximum | Same |
| Loose roll/hip pose hint | +0.5 | Removed |
| Planar speed | -0.5 times base XY speed squared | -2 times (support-wheel speed/0.1)^2, capped raw value4 |
| Fixed support-point drift | None | Quadratic cost up to8 weighted units |
| Stationary contact bonus | None | Up to+2, including both-foot stance |
| Yaw | -0.05 times world yaw rate squared | No direct cost below0.5 rad/s; excess squared cost |
| Swing height ceiling | No upper-height penalty | -2 times (max(height-0.08,0)/0.04)^2 |
| Swing COM XY proximity | None | Up to+1 |
| Wheel proxy overlap | None | Cost up to8 weighted units |

For the same numeric speed, the quadratic coefficient changed from0.5 to200
(400x); reference points also differ (body center versus support wheel), so
this is not a claim that every trajectory's cost increased exactly400x.
The maximum stationary bonus also competes with initial lift acquisition.

Height was never physically capped. Before timestep scaling, the old strict
height cost at10/12/16/20/27 cm is0.5/2/8/18/45.125. The positive lift component
still saturated at+2 above4 cm. Thus the former high-lift strategy became
very expensive. All reward terms share the0.02 s timestep multiplier.

However, in the last20 sampled logs of the failing runs, height-cost magnitude
was only0.95% left /1.05% right of the speed cost. These averages concern the
short completed episodes actually observed; they cannot establish that the
height objective had no effect on exploration. Multiple reward changes were
introduced together, so there is no controlled causal attribution to one term.
Evidence: `one_leg_reward_scale_audit.json`. Logged episode reward sums are
divided by the fixed20 s horizon; they must not be read as instantaneous costs.

## Lift-first objective

Only rewards and diagnostic metrics change in this revision. The10 cm cutoff
stays removed. Base/knee contact failures and20 s timeouts are retained.

| Component | Previous weight | Lift-first weight |
|---|---:|---:|
| Positive lift component | +2 | +4 effective |
| Loose pose hint | absent | +0.5 restored |
| Support-speed penalty | -2 | -0.02 (100x weaker) |
| Support-position penalty | -2 | -0.05 (40x weaker) |
| Height-excess penalty | -2 | -0.05 (40x weaker) |
| Support-leg tilt | -1 | -0.1 (10x weaker) |
| Yaw excess | -0.1 | -0.01 (10x weaker) |
| Wheel proxy overlap | -2 | -0.1 (20x weaker) |
| Action differences | -0.005 | -0.001 (5x weaker) |
| Joint acceleration | -2.5e-7 | -5e-8 (5x weaker) |
| Stationary-contact bonus | +2 | +0.1 (20x weaker) |
| COM-proximity bonus | +1 | +0.1 (10x weaker) |
| Alive | +2 | +2 |
| Failure | -10 | -10 |

The lift gain doubles only the positive clearance component. Grounded swing
and missing support costs keep their old magnitudes; multiplying the entire
signed reward would have unintentionally strengthened those penalties.
At12 cm, the new height penalty is0.05 versus up to4 positive lift units;
at20 cm it is0.45. This permits initial high-lift exploration. Low height and
tucking remain soft preferences rather than conditions for earning lift credit.
There is no automatic curriculum or later tightening in this run.

The original loose pose hint restores broad roll20–40 degrees and both hip
angle magnitudes25–40 degrees. It does not prescribe signs or the full pose.
The saved fixed-entry anchor remains privileged state; exact world anchor
position is not added to actor observations, so precise later position holding
still needs evaluation. Higher lifts and larger motion can occur under the
weaker shaping; first lift is the requested current priority.

## Transition and checks

The previous no-cutoff producers were intentionally interrupted at21230 vector
steps /42260 updates; their complete20k checkpoints and W&B histories remain.
Both producer exits were verified before replacements. Generic trainer reports
FAIL/KeyboardInterrupt; the operator-requested stop is documented in
`one_leg_lift_first_previous_stop.json`, not treated as numerical divergence.

- PASS: 16 tests including real CUDA anchor reset behavior, no drift cutoff,
  legacy reference regression, mirror/playback contract, soft height,
  doubled positive lift credit and unchanged wrong-contact penalties.
  `one_leg_lift_first_tests.log`; three inherited mass/inertia DR warnings.
- PASS: separate fresh left/right CLI probes, each1024 environments, full1M
  replay,16 steps and22 finite learner updates. Minimum replay4096/batch256,
  console logger/no W&B/video are explicit local-only probe overrides.
  `one_leg_lift_first_{left,right}_probe.log`.
- PASS: actual saved native environment comparison finds all non-reward/metric
  settings unchanged from the no-cutoff20k configurations on both sides.
  `one_leg_lift_first_config_comparison.json`.
- Evaluator now records first correct supported lift latency (≥1 cm clearance,
  no swing contact and no failure), fractions lifting within0.5/1/2 s, and which
  knee triggered first-episode failure. Knee flags are captured at the actual
  termination computation before later sensor refresh. Strict original final
  quality criteria remain separate from these lift-acquisition metrics.
- PASS execution / SUSPICIOUS behavior: frozen no-cutoff20k left/right policies,
  16 environments each, seed42, saved noise/DR, first1 s episode. Both16/16
  lift within0.5 s, but all16/16 fail on the SWING-side leg_3 contact; support
  knee and both-knee failure counts are zero. Mean supported lift0.11375 s
  left /0.12750 s right. This identifies the failing side and shows that lift
  initiation alone is not absent; it does not isolate the causal reward term.
  `one_leg_strict_{left,right}_knee_audit.json` and NPZ/log.
- PASS frozen evaluator plumbing: separate untrained16-step lift-first probe,
  4 environments /1 s. It correctly reports first-lift latencies and knee
  side; all four eventually fail. This is NOT learned success.
  `one_leg_lift_first_eval_probe.json` and NPZ/log.
- PASS: source audit finds exactly the three intended source changes and no
  unrelated existing source changes/deletions. Incremental diff inspected;
  `one_leg_lift_first_source_audit.json` and `_incremental.diff`.
- PASS: `./scripts/agent-check.sh`, direct log `one_leg_lift_first_agent_check.log`.
- Actual main startup is recorded below after remote/local verification.

Replacement main plan: independent fresh left/right,1024 environments each,
100000 vector steps, seed42, unchanged FlashSAC/replay settings, W&B online,
checkpoints every5000 and40 s videos every10000 control steps. Label `lift_first`
keeps histories/state/artifacts separate. Final64-environment frozen evaluation
and W&B evidence upload remain scheduled, not yet claimed complete.

Changed source files: `mj_lab/robots/tita/stand_one_leg_anchor_env_cfg.py`,
`test/test_mjlab_one_leg_anchor.py`, `test/evaluate_one_leg_anchor.py`.
Existing runner and trainer registration are reused. Experiment audits/reports
are under this dated directory. No commit, publication or hardware commands.

## Actual main startup

Persistent session `tita_one_leg_lift_first_20261103`, runner PID635787.

| Side | Run ID | PID | Observed step / updates | W&B |
|---|---|---:|---:|---|
| left | tita_mjlab_135938_423332 | 635797 | 100 /2 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/mara6y5w) |
| right | tita_mjlab_135938_442647 | 635798 | 100 /2 | [online](https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/ah2j0h48) |

Both actual argument files have resume=null and warm_start=null. Direct producer
logs confirm finite updates. Remote metrics visibility is recorded separately
in `one_leg_lift_first_wandb_startup.json`. Main checkpoint hashes remain pending
step5000, and populate `one_leg_anchor_lift_first_{left,right}_state.json` after
saving. Startup success does not establish learned quality. Scheduled video
and final assessment uploads are not yet claimed successful.

All short frozen diagnostic/evaluator probes explicitly use local/offline
logging without W&B upload. Main runs use online W&B and the final assessment
uploads its metrics and saved evaluation evidence through the persistent runner.
