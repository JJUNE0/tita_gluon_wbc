# p004_tita_flash_sac_193248_068255_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_193248_068255_model_5000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 4.0
    }
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
  "initial_physics_sha256": "bd1876362faf0d495c5c521d9ce5e87b3d67338fb7805486d7dc3ee484f8f6dc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.24713296117120315,
  "max_drift_m": 0.24887383931880416,
  "radial_IAE_m_s": 13.933406634433563,
  "signed_longitudinal_delta_m": -0.24707266087962493,
  "tail_speed_mean_m_s": 4.709282548903549e-05,
  "tail_speed_rms_m_s": 4.712334916614203e-05,
  "tail_sensor_speed_mean_m_s": 4.234912928498819e-05,
  "tail_fk_speed_mean_m_s": 3.670829848630273e-05,
  "peak_tilt_rad": 0.07523971797388729,
  "peak_wheel_torque_nm": 0.9089967012405396,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.013172987584151,
  "final_integral_m_s": -1.013172987584151,
  "elapsed_wall_s": 4.647409348981455
}
```
