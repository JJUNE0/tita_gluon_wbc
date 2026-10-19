# tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "3547ae91e67bd228ae4a304158fce9982ab9dab3b9ec43a516570ab79fa35e2d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.6265352920770018,
  "max_drift_m": 3.6265352920770018,
  "radial_IAE_m_s": 110.15304600957691,
  "signed_longitudinal_delta_m": 3.5979607225122914,
  "tail_speed_mean_m_s": 0.05889902332457187,
  "tail_speed_rms_m_s": 0.05890004411546252,
  "tail_sensor_speed_mean_m_s": 0.05877130123073976,
  "tail_fk_speed_mean_m_s": 0.05876962134962842,
  "peak_tilt_rad": 0.06291811999886088,
  "peak_wheel_torque_nm": 0.2670959234237671,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.072729942039587
}
```
