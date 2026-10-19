# tita_flash_sac_115632_883848_model_75000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "94f015b9d470467374b6eab3b3342ccb8c9780d87777117294b2fb185217d7eb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0006849424467659272,
  "max_drift_m": 0.0006849424467659272,
  "radial_IAE_m_s": 0.019232658114879446,
  "signed_longitudinal_delta_m": 0.0005313123463770833,
  "tail_speed_mean_m_s": 1.1868776653873489e-05,
  "tail_speed_rms_m_s": 1.2338347870707696e-05,
  "tail_sensor_speed_mean_m_s": 1.1912447710452235e-05,
  "tail_fk_speed_mean_m_s": 1.2566164378657636e-05,
  "peak_tilt_rad": 0.05178728639589192,
  "peak_wheel_torque_nm": 0.03346757963299751,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.005842199390850416,
  "final_integral_m_s": 0.00580328855977697,
  "elapsed_wall_s": 4.478881411952898
}
```
