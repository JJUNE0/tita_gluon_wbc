# tita_flash_sac_193248_068255_model_100000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
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
  "initial_physics_sha256": "a22cef5300eafcfdef4852c2e35e28083149b5d79dfbeb3c4a91badabee9519b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025351559051866215,
  "max_drift_m": 0.038191355871905225,
  "radial_IAE_m_s": 1.512857242944838,
  "signed_longitudinal_delta_m": 0.02535040720728268,
  "tail_speed_mean_m_s": 9.798054229421877e-06,
  "tail_speed_rms_m_s": 9.79814280330951e-06,
  "tail_sensor_speed_mean_m_s": 9.734624197205491e-06,
  "tail_fk_speed_mean_m_s": 9.753157020414613e-06,
  "peak_tilt_rad": 0.05235174120289798,
  "peak_wheel_torque_nm": 0.6483033895492554,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.262503766816265,
  "final_integral_m_s": 0.2624841444435527,
  "elapsed_wall_s": 4.402680141036399
}
```
