# tita_flash_sac_115632_883848_model_85000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "c3ad821a18e209e5b83758c583a3f1f4204a0cd4faaa454283a68eb42eaf29db",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.77142863949761,
  "max_drift_m": 1.77142863949761,
  "radial_IAE_m_s": 53.40804586036192,
  "signed_longitudinal_delta_m": -1.7709960577910924,
  "tail_speed_mean_m_s": -0.029304731261468146,
  "tail_speed_rms_m_s": 0.029304770199319662,
  "tail_sensor_speed_mean_m_s": -0.029241844591794332,
  "tail_fk_speed_mean_m_s": -0.029241881063288882,
  "peak_tilt_rad": 0.05950114283999519,
  "peak_wheel_torque_nm": 0.12557677924633026,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.810689361998811
}
```
