# tita_flash_sac_115632_883848_model_60000_friction0.8_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction0.8_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "649fa84ed8f31213cbefad3bbd95074ed3eeb15f4ae8ec33d0fbd1e1ffa71dd3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9167446084231126,
  "max_drift_m": 0.9167446084231126,
  "radial_IAE_m_s": 27.436328765314595,
  "signed_longitudinal_delta_m": 0.9154109702629322,
  "tail_speed_mean_m_s": 0.015455923281416685,
  "tail_speed_rms_m_s": 0.015458304291346755,
  "tail_sensor_speed_mean_m_s": 0.015422334002316048,
  "tail_fk_speed_mean_m_s": 0.015423822139303326,
  "peak_tilt_rad": 0.07035929965112375,
  "peak_wheel_torque_nm": 0.12384442239999771,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.408741757040843
}
```
