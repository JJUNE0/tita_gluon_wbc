# tita_flash_sac_193248_068255_model_5000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "7a3885da3dae1de421328a0831e7380f51423fda3873039a4d146393e4b8bc53",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.20210415265192586,
  "max_drift_m": 0.20383782182575777,
  "radial_IAE_m_s": 11.560999645959699,
  "signed_longitudinal_delta_m": -0.20205823993013663,
  "tail_speed_mean_m_s": 3.6944032748072955e-05,
  "tail_speed_rms_m_s": 3.6972162382272014e-05,
  "tail_sensor_speed_mean_m_s": 3.168865767700257e-05,
  "tail_fk_speed_mean_m_s": 2.5882625617595022e-05,
  "peak_tilt_rad": 0.07519944895259645,
  "peak_wheel_torque_nm": 0.9056823253631592,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0138888506989474,
  "final_integral_m_s": -1.0138888506989474,
  "elapsed_wall_s": 12.403119865979534
}
```
