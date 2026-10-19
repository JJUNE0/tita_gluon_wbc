# tita_flash_sac_193248_068255_model_100000_com-0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com-0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "1c399982d6a99a6e69875d93044de2c33fa35a1e972c2ac4dfd229aaff3b46ec",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012900418777089534,
  "max_drift_m": 0.01634084989138983,
  "radial_IAE_m_s": 0.7330677846458187,
  "signed_longitudinal_delta_m": 0.012899414972773656,
  "tail_speed_mean_m_s": 2.5101638754824457e-05,
  "tail_speed_rms_m_s": 2.5113256715979768e-05,
  "tail_sensor_speed_mean_m_s": 2.500343984137779e-05,
  "tail_fk_speed_mean_m_s": 2.502059230182459e-05,
  "peak_tilt_rad": 0.045388689550364125,
  "peak_wheel_torque_nm": 0.2547520697116852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1320126513471256,
  "final_integral_m_s": 0.13196229551378555,
  "elapsed_wall_s": 5.4213835499831475
}
```
