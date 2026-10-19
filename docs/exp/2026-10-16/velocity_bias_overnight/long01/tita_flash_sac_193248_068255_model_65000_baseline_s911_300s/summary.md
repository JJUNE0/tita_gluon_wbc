# tita_flash_sac_193248_068255_model_65000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "82f7e93ec854dfb9f4baa53a9dc4a70ec893e8ff1cc6ef9c627c86a8fc661e45",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 11.812521981148096,
  "max_drift_m": 11.812521981148096,
  "radial_IAE_m_s": 1845.4836495449338,
  "signed_longitudinal_delta_m": -11.207727455327987,
  "tail_speed_mean_m_s": -0.03758431826564079,
  "tail_speed_rms_m_s": 0.03758437835941438,
  "tail_sensor_speed_mean_m_s": -0.03750297627510575,
  "tail_fk_speed_mean_m_s": -0.03749846257260053,
  "peak_tilt_rad": 0.02944055482045216,
  "peak_wheel_torque_nm": 0.04873155057430267,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 62.53699149203021
}
```
