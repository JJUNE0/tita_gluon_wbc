# Inspection hub graph build

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `SUSPICIOUS`
- Policy Checkpoint SHA256: `N/A` (offline geometry job)
- Graph NPZ SHA256:
  `2e857b784b97ce5eff58738f8a8f03d808cf17f9ccf4004cce31db4fda226fd9`
- Graph metadata JSON SHA256:
  `59c4cca3135359e0c5a57dc458ea3c36b659ce871b834d02490647c84a1a31a0`

## Command and result

```text
/home/cocel/isaac/env_isaaclab/bin/python \
  test/build_tita_gluon_cartesian_hub_graph.py \
  --max-targets 256 \
  --collision-clearance-m 0.01 \
  --progress-every 250
```

```text
TITA_GLUON_CARTESIAN_GRAPH,domain=VALIDATION_SIM,status=SUSPICIOUS,
targets=256,edges=256,max_distance_m=0.421511
```

The builder checked every stored WORK-to-hub interpolation with no more than
2 degrees between joint samples, at least 10 degrees endpoint/path joint
margin, translational `sigma_min >= 0.015`, and Pinocchio/hpp-fcl collision
queries over three TITA stand/reset-envelope postures. The source and output
metadata contain the current combined and standalone URDF hashes.

The selected task nodes are:

| Task pose | Graph node | TITA-base EE position (m) |
|---|---:|---|
| LEFT_HIGH | 23 | `[-0.126, 0.196, 0.546]` |
| RIGHT_LOW | 111 | `[0.200, -0.180, 0.352]` |
| LEFT_LOW | 18 | `[0.242, 0.142, 0.304]` |
| RIGHT_HIGH | 208 | `[0.167, -0.216, 0.571]` |

`SUSPICIOUS` is retained because 10 mm is a simulation admission margin, the
mount/collision geometry is provisional, wheel-leg pairs and the ground are
outside the claimed safety set, only three TITA postures were checked, and no
gripper/tool model is present. This is an offline mesh-validated graph, not a
formal collision-free certificate.
