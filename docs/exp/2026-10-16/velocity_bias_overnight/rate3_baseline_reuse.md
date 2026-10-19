Execution Domain: VALIDATION_SIM / DESKTOP_DRY_RUN

Policy Checkpoint SHA256 (reference): 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05; all 40 hashes in checkpoint_manifest.json.

Evidence Status: NOT_TESTED until comparisons are audited.

rate3_long01 reuses the already completed zero-bias baselines in seeded_long01: identical policy/config, seed918, 1.2 s acquisition, flat nominal physics and 300 s horizon. rate3_extended01 reuses extended_nominal01 zero-bias baselines at seed914/900 s. rate3_primary01 reuses the matched primary baseline/M4 traces at seed913. Every reused pair must pass the exact initial qpos/qvel/raw-last-action hash check. The repeated-time observer fix does not change ordinary once-per-step acquisitions. Source snapshots and policy exports remain preserved. Reuse avoids re-running a physically identical baseline; relative performance claims are withheld if a pair fails the hash check.
