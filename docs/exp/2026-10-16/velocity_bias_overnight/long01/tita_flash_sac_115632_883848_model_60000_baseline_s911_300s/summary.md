# tita_flash_sac_115632_883848_model_60000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
  "state_columns": [
    "base_x",
    "base_y",
    "base_z",
    "base_forward_speed",
    "roll",
    "pitch",
    "yaw",
    "raw_position",
    "raw_speed",
    "fk_position",
    "fk_speed"
  ],
  "initial_physics_sha256": "4fa09250b2e3cc4fc8399d53bc785f070ef3b1f1301eab90b6d72b77744cbeed",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 5.329524346745874,
  "max_drift_m": 5.329524346745874,
  "radial_IAE_m_s": 763.5519374691667,
  "signed_longitudinal_delta_m": 5.2563567613664235,
  "tail_speed_mean_m_s": 0.01948044768074193,
  "tail_speed_rms_m_s": 0.01948046649271153,
  "tail_sensor_speed_mean_m_s": 0.019437838754195358,
  "tail_fk_speed_mean_m_s": 0.019439144685779102,
  "peak_tilt_rad": 0.06981453979283092,
  "peak_wheel_torque_nm": 0.15213868021965027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 41.52566318202298
}
```
