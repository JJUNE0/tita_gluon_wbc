# tita_flash_sac_115632_883848_model_60000_mass130_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "f01d75275d2e16bfe7d07d51ad721924a15f67360825dc322e6df0ba697a6b17",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 16.465476819500818,
  "max_drift_m": 19.080670718155453,
  "radial_IAE_m_s": 4284.233771060624,
  "signed_longitudinal_delta_m": -15.247908308527286,
  "tail_speed_mean_m_s": -0.0858527872671442,
  "tail_speed_rms_m_s": 0.08585279679206573,
  "tail_sensor_speed_mean_m_s": -0.08516756056242027,
  "tail_fk_speed_mean_m_s": -0.08540332236563801,
  "peak_tilt_rad": 0.06652045729433076,
  "peak_wheel_torque_nm": 0.25966811180114746,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 52.14406134095043
}
```
