# tita_flash_sac_193248_068255_model_5000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "087653dd08268d3b13977975e6ceb27df4dc5fe7087f129208b04f4c15b0180a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1946364863018178,
  "max_drift_m": 0.1946364863018178,
  "radial_IAE_m_s": 10.340829456394154,
  "signed_longitudinal_delta_m": -0.18110088290533688,
  "tail_speed_mean_m_s": 0.0005757807030249518,
  "tail_speed_rms_m_s": 0.0005814979856131407,
  "tail_sensor_speed_mean_m_s": 0.0004108585834291071,
  "tail_fk_speed_mean_m_s": 0.0003554823439682701,
  "peak_tilt_rad": 0.07450060206832165,
  "peak_wheel_torque_nm": 0.6406423449516296,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.9895405451934417,
  "final_integral_m_s": -0.9895405451934417,
  "elapsed_wall_s": 14.667850158002693
}
```
