# tita_flash_sac_193248_068255_model_30000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "559358cbb5656f607589164e0383af9cf04bd854c9e1247656c191aa3cc39d95",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010569917706456591,
  "max_drift_m": 0.016924689561917904,
  "radial_IAE_m_s": 0.6410470191876992,
  "signed_longitudinal_delta_m": 0.010566345408795587,
  "tail_speed_mean_m_s": -4.478725664103174e-06,
  "tail_speed_rms_m_s": 5.624818059854246e-06,
  "tail_sensor_speed_mean_m_s": -4.227215264048121e-06,
  "tail_fk_speed_mean_m_s": -4.539112730862698e-06,
  "peak_tilt_rad": 0.01989255908269416,
  "peak_wheel_torque_nm": 0.4173518717288971,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10990476499392322,
  "final_integral_m_s": 0.10992079262974055,
  "elapsed_wall_s": 5.83594986400567
}
```
