# tita_flash_sac_193248_068255_model_85000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "0e411dd38f76df0acff629b71e96036eb5f456d42be2edf63a551b887bcfdd05",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024814514999228588,
  "max_drift_m": 0.045497239477600475,
  "radial_IAE_m_s": 1.4110965812113674,
  "signed_longitudinal_delta_m": 0.02481448244801491,
  "tail_speed_mean_m_s": 4.65638917456921e-05,
  "tail_speed_rms_m_s": 4.6567678221840224e-05,
  "tail_sensor_speed_mean_m_s": 4.652126170680571e-05,
  "tail_fk_speed_mean_m_s": 4.625989032754114e-05,
  "peak_tilt_rad": 0.06387939055718506,
  "peak_wheel_torque_nm": 0.803718090057373,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.25546101926107284,
  "final_integral_m_s": 0.255370613533301,
  "elapsed_wall_s": 14.428886893030722
}
```
