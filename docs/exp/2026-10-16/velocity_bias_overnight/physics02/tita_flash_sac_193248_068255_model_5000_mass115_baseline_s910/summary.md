# tita_flash_sac_193248_068255_model_5000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "842cdbd61c227c1e25246bc270fddb36533603ad8e4b5f728ecdf18b62acce5c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.791025512581235,
  "max_drift_m": 3.791025512581235,
  "radial_IAE_m_s": 122.75507028990378,
  "signed_longitudinal_delta_m": -3.4320323070432677,
  "tail_speed_mean_m_s": -0.06295136222374344,
  "tail_speed_rms_m_s": 0.06295362175347254,
  "tail_sensor_speed_mean_m_s": -0.06310655416017343,
  "tail_fk_speed_mean_m_s": -0.06324111369863054,
  "peak_tilt_rad": 0.06540095817273439,
  "peak_wheel_torque_nm": 2.0653789043426514,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.777955905999988
}
```
