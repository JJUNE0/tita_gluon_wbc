# TITA FlashSAC run

Execution Domain: TRAINING_SIM

Evidence Status: BLOCKED

Policy Checkpoint SHA256 (actor.pt): N/A (no checkpoint produced)

Task: `DDT-Velocity-Flat-Tita-My-v0`

Vector steps: 0 -> 0; learner updates this run: 0.

Observed behavior / log summary: ImportError: cannot import name 'CoRlHybridPpoActorCriticCfg' from 'scripts.co_rl.core.wrapper' (/home/cocel/Desktop/Research/wolf-quadruped/rl/wolf-stair-rl/scripts/co_rl/core/wrapper/__init__.py)

Checkpoint: `None`

Actor uses policy observations; critic uses its independent privileged group. PPO velocity estimator is absent. Training completion does not establish locomotion quality.
