# Position-only stop-and-go Gate validation

- Execution Domain: `VALIDATION_SIM`
- Evidence Status: `PASS` for the position-only four-target prerequisite
- Policy checkpoint: `model_9000.pt`
- Policy checkpoint SHA256: `9d8d1fad8f0e2c3e04eb9d937ca91706174ea8b97c21501eb6b2744defc8acde`
- Safety configuration: self-collision disabled, CBF disabled

## Scope

This run validates the deterministic stop-and-go execution contract before
concurrent scheduling or high-level RL. The four ordered targets use
gravity-aligned route positions, position-only local differential IK, a
base-relative graph executor, and the frozen arm-state-conditioned TITA
locomotion checkpoint. It does not validate orientation tracking, mesh
collision avoidance, or a safety guarantee.

The validation-only graph profile was 60 deg/s and 180 deg/s^2. The base was
commanded to zero velocity during graph execution, local target servo, and
dwell. A measured stop gate required planar speed at most 0.03 m/s and yaw
rate at most 0.05 rad/s before accepting `EXECUTE_CURRENT`.

## Root causes corrected

1. The graph executor read a live graph-phase tensor while advancing completed
   environments. Starting phase 2 mutated that tensor, allowing phase 2 to be
   marked complete in the same control update. A phase snapshot now separates
   STOW and hub completion.
2. The old stop-and-go controller still issued up to 0.15 m/s during arm
   execution. It now holds a zero base command and checks measured motion
   before local target execution.
3. Position-only mode now uses only the translational Jacobian instead of
   retaining zero-weight angular constraints.
4. Route target translation is gravity-aligned rather than tilted by the
   settled base roll/pitch.
5. Offline graph nodes outside IsaacLab's 0.8 soft joint limits are removed
   from the runtime catalog; 213 of 257 nodes remain.

## Evidence

### Fixed-root executor smoke

- Environments: 2
- Physics steps: 1,157
- Result: target completion in both environments
- Maximum graph joint tracking error: 0.0570 rad
- Log: `graph_phase_snapshot_executor_smoke_60deg.log`

### One-environment end-to-end run

- Seed: 20260811
- Success: 1/1
- Cycle time: 49.880 s
- Falls / base contacts / timeouts: 0 / 0 / 0
- Local-region exits: 0
- Result: `model9000_position_only_four_target_60deg_validation.json`

### Eight-environment held-out run

- Seed: 20260812
- Success: 8/8
- Mean successful cycle time: 50.765 s
- Cycle-time range: 49.780--51.960 s
- Falls / base contacts / timeouts: 0 / 0 / 0
- Local-region exits / option rejections: 0 / 0
- Final target index: 4 for all eight environments
- Maximum tilt norm by environment: 0.235--0.261
- Maximum absolute base-height deviation by environment: 0.041--0.048 m
- Result: `model9000_position_only_four_target_8env_seed20260812.json`

The combined end-to-end evidence is 9/9 successful episodes over two seeds.
The concurrent-motion ratio is correctly zero for this stop-and-go baseline.

## Interpretation and unresolved risks

The position-only deterministic prerequisite passes and unblocks the tuned
concurrent scheduler experiment. It does not yet unblock a collision-safety
claim or hardware execution.

- The 60 deg/s graph profile is a validation override and exceeds the 20 deg/s
  arm-motion distribution used during low-level training.
- Orientation/facing and q6 behavior remain unvalidated in this task.
- The local regions and graph are not yet dense-mesh validated with the final
  mount/tool geometry.
- Self-collision and CBF are disabled; successful task execution is not
  evidence of collision-free execution.
- Peak simulated tilt and height excursions should remain diagnostic metrics
  when scheduler overlap is introduced.

The next Gate-0 step is to grid-search the deterministic concurrent scheduler
on training layouts, freeze its parameters, and evaluate it on held-out
layouts before training the hybrid high-level PPO policy.
