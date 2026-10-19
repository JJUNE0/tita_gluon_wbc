Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: see checkpoint_manifest.json for all 40.

Evidence Status: FAIL / SUSPICIOUS

entry01 and entry_physics01 fail at t=0 before applying controller because RL begins crouched below the standing guard. These are invalid early-activation tests, not evidence of controller failure. Keep all failures. entry02 uses the existing standing guard after a common 1.2 s baseline acquisition.

entry_physics01 mass13 jobs used unknown mass_scale key, silently ignored by StaticEnv. They are nominal duplicates and must not support a mass robustness claim. Unknown physics keys now raise an error. Earlier physics_pilot_v01 used correct mass key and remains valid.
