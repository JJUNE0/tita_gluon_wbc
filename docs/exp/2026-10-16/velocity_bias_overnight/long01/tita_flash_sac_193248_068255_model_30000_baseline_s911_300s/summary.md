# tita_flash_sac_193248_068255_model_30000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "ba6028e06d4c50e1c066e3416e783ba12cd607b8b0206ed2b32fa1b6fb317885",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 14.285234291467539,
  "max_drift_m": 14.285234291467539,
  "radial_IAE_m_s": 2156.977893892317,
  "signed_longitudinal_delta_m": 14.113549835736972,
  "tail_speed_mean_m_s": 0.047656562304454586,
  "tail_speed_rms_m_s": 0.047656562583712404,
  "tail_sensor_speed_mean_m_s": 0.047553548411581,
  "tail_fk_speed_mean_m_s": 0.04755253909077587,
  "peak_tilt_rad": 0.019996055118842504,
  "peak_wheel_torque_nm": 0.15195484459400177,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 49.785978142987005
}
```
