# RMA teacher oracle-free model 9999 observation-order audit

- Date: 2026-08-20
- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` (observation ordering), `SUSPICIOUS` (asymmetric policy target remains)
- Checkpoint: `/home/cocel/Desktop/Research/isaaclab_add_reward_autotuning/logs/co_rl/Tita_Flat_Stand_Drive-v3-mooppo/mooppo/2026-08-20_13-58-18_rma_teacher_oracle_free_stack0_corrected_10k/model_9999.pt`
- Checkpoint SHA256: `efff7f99f3eb1a99f6bd06c37fae7b6b46c26ae7b75f3bdf41492304c6f46eea`
- Actor ONNX SHA256: `d1f97d24f2adbccff4b9ec6f9bec9c0df51bf8aa68ea97bf0fcc2e41a8041686`
- Encoder ONNX SHA256: `f5626236dc23bd76ff9c4c4900d7658a350870a518dcbe738026c0f2c967aec2`

## Result

No functional observation-order mismatch was found. A headless one-environment
Isaac Lab probe of `Isaac-Velocity-Flat-Tita-RMATeacher-TargetHeight-v3-moo-ppo`
reported the runtime articulation order as:

```text
[L1, R1, L2, R2, L3, R3, L4, R4]
```

The ObservationManager resolved the combined hip/shoulder position and velocity
terms to joint IDs `[0, 1, 2, 3]`, the leg terms to `[4, 5]`, and the wheel term
to `[6, 7]`. This agrees with the MuJoCo-side reindex arrays.

The 32-dimensional actor proprioceptive observation is therefore:

| Slice | Term | Joint/channel order |
|---|---|---|
| `0:4` | hip/shoulder position | `L1, R1, L2, R2` |
| `4:6` | leg position | `L3, R3` |
| `6:10` | hip/shoulder velocity x 0.05 | `L1, R1, L2, R2` |
| `10:12` | leg velocity x 0.05 | `L3, R3` |
| `12:14` | wheel velocity x 0.05 | `L4, R4` |
| `14:17` | base angular velocity x 0.25 | `x, y, z` |
| `17:20` | projected gravity | `x, y, z` |
| `20:28` | previous raw action | `L1, R1, L2, R2, L3, R3, L4, R4` |
| `28:32` | command | `2*vx, vy, 0.25*wz, normalized height` |

The 26-dimensional teacher privileged observation also agrees with training:

```text
contact(L4,R4), base mass*0.1, base CoM xyz*10,
Kp(L1,R1,L2,R2,L3,R3,L4,R4)*0.01,
Kd(L1,R1,L2,R2,L3,R3,L4,R4),
base velocity xyz*(2,1,0.25), base height
```

## Live MuJoCo evidence

With the running viewer in `rl_0`, MuJoCo native joint state order was
`[L1,L2,L3,L4,R1,R2,R3,R4]`. A simultaneous sample contained:

```text
native:    L1=0.00220, L2=1.12798, R1=0.02433, R2=0.60101,
           L3=-1.74530, R3=-1.64543
actor obs: 0.00220, 0.02433, 1.12798, 0.60101, -1.74530, -1.64543
```

This is the expected native-to-Isaac reorder. Actor observation slots `20:28`
also matched `/cosim_ros2_jazzy/debug/action_raw` sample-for-sample.

The asymmetric joint posture is currently commanded by the policy itself, not
introduced by the output adapter. At the same steady sample, policy/raw order
was approximately:

```text
[L1=0.04861, R1=-0.03573, L2=1.11346, R2=0.63678,
 L3=-1.52413, R3=-1.40618, L4=0.05680, R4=-0.05744]
```

The native joint target topic contained the corresponding correctly reordered
position targets. The next diagnosis should compare teacher latent inputs and
outputs against an Isaac Lab rollout at the same state, rather than changing
the proprioceptive joint ordering.

## Checks executed

- Isaac Lab runtime articulation/ObservationManager order probe: `PASS`
- Live ROS 2 `/joint_states`, `/debug/obs_current`, `/debug/action_raw`, and
  `/debug/joint_target` comparison: `PASS`
- `python3 -m pytest -q test/test_rma_privileged_obs_v5.py`: `PASS` (`2 passed`)

## Known documentation issue

`MooStandDriveObservationBuilder` has a stale paragraph that describes the
Isaac articulation native order as left-chain-first. The executable constants
and mappings are correct; only that paragraph is contradictory. It was not
changed during this read-only diagnostic task.
