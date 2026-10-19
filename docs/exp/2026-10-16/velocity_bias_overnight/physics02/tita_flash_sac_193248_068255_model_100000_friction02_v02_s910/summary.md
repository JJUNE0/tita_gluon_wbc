# tita_flash_sac_193248_068255_model_100000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
    },
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
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "c9dba37b5697fbeac062f0f65c656a6f325b8921729b7dcd87a5b671c9499af2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02738939374786248,
  "max_drift_m": 0.03759124833572537,
  "radial_IAE_m_s": 1.6310530760557223,
  "signed_longitudinal_delta_m": 0.027385886292210813,
  "tail_speed_mean_m_s": 9.714265364523984e-06,
  "tail_speed_rms_m_s": 9.9191533035837e-06,
  "tail_sensor_speed_mean_m_s": 9.720177706218816e-06,
  "tail_fk_speed_mean_m_s": 9.638918356866185e-06,
  "peak_tilt_rad": 0.052498474115477034,
  "peak_wheel_torque_nm": 0.650600790977478,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27418783782675693,
  "final_integral_m_s": 0.27415283410786373,
  "elapsed_wall_s": 23.3260554500157
}
```
