# tita_flash_sac_193248_068255_model_30000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "513f43c99ddcc01c27b94a780f127a3d069d6cfd961ffdba71ebf5590779e811",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010548013818750777,
  "max_drift_m": 0.017942201371817693,
  "radial_IAE_m_s": 0.6410202563536362,
  "signed_longitudinal_delta_m": 0.010544412975218916,
  "tail_speed_mean_m_s": -5.689429061600544e-06,
  "tail_speed_rms_m_s": 6.407682910451336e-06,
  "tail_sensor_speed_mean_m_s": -5.445151261769923e-06,
  "tail_fk_speed_mean_m_s": -5.74685753054004e-06,
  "peak_tilt_rad": 0.020026950865556392,
  "peak_wheel_torque_nm": 0.35453522205352783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10967113595359552,
  "final_integral_m_s": 0.10968697486736816,
  "elapsed_wall_s": 14.38357237301534
}
```
