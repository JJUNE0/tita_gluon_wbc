# tita_flash_sac_193248_068255_model_30000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "4afe13a5f0c1c3d55dfc7d01ae4051e263134fce4b3343b270d628ac95f674cf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.9248672545384458,
  "max_drift_m": 2.9248672545384458,
  "radial_IAE_m_s": 88.15296839482119,
  "signed_longitudinal_delta_m": 2.9237901523416783,
  "tail_speed_mean_m_s": 0.04829746880567905,
  "tail_speed_rms_m_s": 0.04829763792185195,
  "tail_sensor_speed_mean_m_s": 0.04819266123671192,
  "tail_fk_speed_mean_m_s": 0.048191386386022966,
  "peak_tilt_rad": 0.01662186478169314,
  "peak_wheel_torque_nm": 0.03153654932975769,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.395079015986994
}
```
