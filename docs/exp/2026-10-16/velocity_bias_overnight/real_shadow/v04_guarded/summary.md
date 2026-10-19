# Passive real-log velocity-bias replay

Execution Domain: DESKTOP_DRY_RUN

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS (replay only)

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "DESKTOP_DRY_RUN",
  "evidence_status": "PASS",
  "run": "flashsac_60000_223217_076704901_output_true",
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "bag_sha256": "50cf02dc232ba981e7817d0cc77ba4df9ab5f440676c3a0c6ae5f896632d910e",
  "parameters": {
    "kp": 0.0,
    "ki": 4.0,
    "tau": 0.1,
    "ramp": 0.25,
    "sign": 1.0,
    "limit": 2.0,
    "slew": 3.0,
    "seed_gain": 3.0
  },
  "samples": 5501,
  "active_samples": 1684,
  "runtime_guard": true,
  "eligible_samples": 1251,
  "raw_active_mean_m_s": -0.1017386850694749,
  "fk_active_mean_m_s": -0.09975957267947747,
  "bias_min_m_s": -2.0,
  "bias_max_m_s": 2.0,
  "no_robot_commands": true,
  "original_bag_unchanged": true,
  "limitations": [
    "Replay uses observed baseline states; no corrected hardware trajectory is inferred.",
    "No chassis ground truth; wheel slip and sensor-frame assumptions remain unvalidated.",
    "Nearest receipt-time alignment is not hardware synchronization."
  ]
}
```
