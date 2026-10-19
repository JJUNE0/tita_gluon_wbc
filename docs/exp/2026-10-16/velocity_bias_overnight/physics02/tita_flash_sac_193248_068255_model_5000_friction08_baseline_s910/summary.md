# tita_flash_sac_193248_068255_model_5000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "8bb1f8970e6c354f061d2ee353c4ecf57d50b7ff5e91cff71ad4e6f991541528",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2205474450295122,
  "max_drift_m": 1.5370580856080092,
  "radial_IAE_m_s": 66.52138039100514,
  "signed_longitudinal_delta_m": 0.02009854792344251,
  "tail_speed_mean_m_s": -0.04307858543040384,
  "tail_speed_rms_m_s": 0.04309972388791951,
  "tail_sensor_speed_mean_m_s": -0.04378780826396137,
  "tail_fk_speed_mean_m_s": -0.044196352907177855,
  "peak_tilt_rad": 0.09080826241455675,
  "peak_wheel_torque_nm": 0.8063728213310242,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.215902945026755
}
```
