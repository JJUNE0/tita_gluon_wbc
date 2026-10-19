# tita_flash_sac_193248_068255_model_5000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "9f05ae5a422e1baed17d1b756b368e434c8a232b69617c6c38dcc42859f01e0c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.2904393985867064,
  "max_drift_m": 3.2904393985867064,
  "radial_IAE_m_s": 99.08947276795634,
  "signed_longitudinal_delta_m": -3.2019604450611814,
  "tail_speed_mean_m_s": -0.05556096262698597,
  "tail_speed_rms_m_s": 0.05556116031874358,
  "tail_sensor_speed_mean_m_s": -0.055529877019489214,
  "tail_fk_speed_mean_m_s": -0.055553247854911725,
  "peak_tilt_rad": 0.06927267211751387,
  "peak_wheel_torque_nm": 0.7467564940452576,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.310812067997176
}
```
