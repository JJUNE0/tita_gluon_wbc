# tita_flash_sac_193248_068255_model_5000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "eb73435498c4ebbcd879e2eeaffe825d89bfae84c3f5e0751006370a044a2fa3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9406770998880565,
  "max_drift_m": 3.9406770998880565,
  "radial_IAE_m_s": 127.29850051823962,
  "signed_longitudinal_delta_m": -3.70594117080682,
  "tail_speed_mean_m_s": -0.06358214734946548,
  "tail_speed_rms_m_s": 0.06358999143994337,
  "tail_sensor_speed_mean_m_s": -0.06376598373593136,
  "tail_fk_speed_mean_m_s": -0.06388712470454251,
  "peak_tilt_rad": 0.06536126901205974,
  "peak_wheel_torque_nm": 2.0689141750335693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.920466338982806
}
```
