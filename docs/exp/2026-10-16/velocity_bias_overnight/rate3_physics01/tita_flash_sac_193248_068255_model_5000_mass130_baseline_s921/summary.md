# tita_flash_sac_193248_068255_model_5000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "a3dbb9e750baa2b4e59f99c861608e24b98d9977d2b1a535b47c233da24dd16d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.075712601696948,
  "max_drift_m": 10.075712601696948,
  "radial_IAE_m_s": 302.942274574071,
  "signed_longitudinal_delta_m": -9.905727301037944,
  "tail_speed_mean_m_s": -0.1686994203089675,
  "tail_speed_rms_m_s": 0.16870517989781406,
  "tail_sensor_speed_mean_m_s": -0.16837579138366582,
  "tail_fk_speed_mean_m_s": -0.1683662267455504,
  "peak_tilt_rad": 0.02196162620414986,
  "peak_wheel_torque_nm": 2.7246310710906982,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.944427045993507
}
```
