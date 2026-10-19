# tita_flash_sac_193248_068255_model_30000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "d71362303e21cbf731a79bdc973f29dd9186a57b4926901be8702af8278fb89e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.504741639417709,
  "max_drift_m": 3.504741639417709,
  "radial_IAE_m_s": 108.08567837014479,
  "signed_longitudinal_delta_m": 3.503471936957279,
  "tail_speed_mean_m_s": 0.05569996567670962,
  "tail_speed_rms_m_s": 0.05570075291294642,
  "tail_sensor_speed_mean_m_s": 0.05562860929226981,
  "tail_fk_speed_mean_m_s": 0.05563020039763026,
  "peak_tilt_rad": 0.03650782195840718,
  "peak_wheel_torque_nm": 0.10737985372543335,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.776569182984531
}
```
