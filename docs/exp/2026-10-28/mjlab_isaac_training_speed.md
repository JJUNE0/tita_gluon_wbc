# mjlab / Isaac Lab measured training speed

Execution Domain: TRAINING_SIM

Evidence Status: PASS for log-derived measurements. Controlled engine-only benchmarking is NOT_TESTED.

Policy Checkpoint SHA256:
- Isaac flat: `83b266e64ffce1d32cd6c7530a673e3d44a9e0705fa0ede72e4bb4c324200b68`
- Isaac walk: `3ec4745778cd8cbcdc4338915ca86ae1f6bc7067f3f583918b42a9c7f9c86aa1`
- mjlab flat: `f71449f130dd4f37b0281324b1e112d2a62bf8a988a91ae8e6b45fe97d244d3b`
- mjlab walk: `0868450122ce8a8e41ae04e42c0b1ff2d0567ffcad3f9c27e35315aef4f18913`
- mjlab hybrid: `N/A (training in progress; first checkpoint pending)`

Observed Metrics / Behavior / Log Summary:

Observed at: 2026-10-28T08:55:33.692965+09:00

| Run | Environments | Transitions/s | Vector steps/s | 100k loop minutes |
|---|---:|---:|---:|---:|
| Isaac flat | 4096 | 48338 | 11.80 | 141.2 |
| Isaac walk | 1024 | 12770 | 12.47 | 133.6 |
| mjlab flat | 1024 | 16675 | 16.28 | 102.3 |
| mjlab walk | 1024 | 16496 | 16.11 | 103.5 |
| mjlab hybrid | 1024 | 16149 | 15.77 | 105.7 (early estimate) |

Matched walk runs both used 1,024 environments, batch 2,048, two SAC updates/vector step, 1M replay, no compile/AMP and videos every 10k vector steps. Observed mjlab throughput was 1.292 times Isaac (29.2% higher), giving 22.6% less loop time for 100k vector steps.

The saved throughput is cumulative transitions / training-loop wall time. It includes simulation, learner work and effects of intermediate checkpoint/video activity. Simulator initialization and final post-loop save/video/upload cleanup are excluded. One vector step advances all environments; 100k steps at 1,024 envs contains 102.4M transitions. These measurements do not isolate physics-engine speed or eliminate background host load.

Important qualification for the existing flat comparison: Isaac flat used 4,096 environments, whereas mjlab flat used 1,024. Their 48.3k vs 16.7k transitions/s numbers are not matched-batch engine measurements. Isaac flat 100k vector steps also collected four times as many transitions. Do not interpret the existing flat throughput panel as Isaac being three times faster under equal settings.

The current hybrid run is ongoing. Its projected duration is an early estimate and can change as contact/reset behavior and video activity evolve. No training settings or production code were changed for this analysis.

Sources:
- Isaac flat: `docs/exp/2026-10-19/tita_flash_sac_173757_852342_metrics.jsonl`, corresponding `_args.json`.
- Isaac walk: `docs/exp/2026-10-27/tita_flash_sac_214239_278101_metrics.jsonl`, corresponding `_args.json`.
- mjlab flat: `docs/exp/2026-10-27/tita_mjlab_235721_754659_metrics.jsonl`, corresponding `_args.json`.
- mjlab walk: `docs/exp/2026-10-28/tita_mjlab_014010_434558_metrics.jsonl`, corresponding `_args.json`.
- mjlab hybrid: `docs/exp/2026-10-28/tita_mjlab_085110_097268_metrics.jsonl`, corresponding `_args.json`.

Branch: `agent/codex/tita-walk`. Only this report and measurement snapshot were created.
