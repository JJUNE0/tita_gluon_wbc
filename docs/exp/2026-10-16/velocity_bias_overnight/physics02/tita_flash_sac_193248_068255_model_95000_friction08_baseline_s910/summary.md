# tita_flash_sac_193248_068255_model_95000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "c014e691810283e6555f777a30322303dda847acc3efd14a37a0398c54861723",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.650119043560053,
  "max_drift_m": 10.650119043560053,
  "radial_IAE_m_s": 271.1781966963888,
  "signed_longitudinal_delta_m": -9.760220390602203,
  "tail_speed_mean_m_s": -0.25463737888680615,
  "tail_speed_rms_m_s": 0.2563384600628653,
  "tail_sensor_speed_mean_m_s": -0.25430095531639796,
  "tail_fk_speed_mean_m_s": -0.25432848277085,
  "peak_tilt_rad": 0.044884901570053426,
  "peak_wheel_torque_nm": 0.19924712181091309,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 19.569166501984
}
```
