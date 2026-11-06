# mjlab / Isaac Lab FlashSAC comparison

Execution Domain: VALIDATION_SIM

Evidence Status: PASS

Policy Checkpoint SHA256:
- flat / Isaac Lab: `83b266e64ffce1d32cd6c7530a673e3d44a9e0705fa0ede72e4bb4c324200b68`
- flat / mjlab: `f71449f130dd4f37b0281324b1e112d2a62bf8a988a91ae8e6b45fe97d244d3b`
- walk / Isaac Lab: `3ec4745778cd8cbcdc4338915ca86ae1f6bc7067f3f583918b42a9c7f9c86aa1`
- walk / mjlab: `0868450122ce8a8e41ae04e42c0b1ff2d0567ffcad3f9c27e35315aef4f18913`

Observed metrics / behavior / log summary:

Learning curves use each engine's own training environment. This is a one-seed comparison, not a controlled claim that one simulator is better.
Reward totals depend on episode length and reward design. Contact friction/damping and some randomization differ; throughput includes shared-host load.
Solid curves average the trailing 20 logged samples; faint curves show raw samples. The CSV preserves the unaligned original step samples.

![mjlab_flat_walk_20261027_224638_flat_comparison](mjlab_flat_walk_20261027_224638_flat_comparison.png)
![mjlab_flat_walk_20261027_224638_walk_comparison](mjlab_flat_walk_20261027_224638_walk_comparison.png)
- flat / Isaac Lab, final 20 log samples: return=52.16265804502368, episode length=997.7060000000001, linear error=0.40289874374866486, yaw error=0.5862466663122177
- flat / mjlab, final 20 log samples: return=42.33292913326621, episode length=955.6115, linear error=0.4824502348899841, yaw error=0.6424360364675522
- walk / Isaac Lab, final 20 log samples: return=108.21376095199587, episode length=999.9069999999999, linear error=0.2652363896369934, yaw error=0.4589955613017082
- walk / mjlab, final 20 log samples: return=76.02757541561128, episode length=998.874, linear error=0.2595053732395172, yaw error=0.44888386577367784

Full metrics and source hashes: `/home/cocel/Desktop/Research/tita_gluon_wbc/docs/exp/2026-10-28/mjlab_flat_walk_20261027_224638_comparison.json`
W&B: https://forge.coreweave.com/wandb/bjy6614-postech/tita_flat_flash_sac/runs/s7wades1
