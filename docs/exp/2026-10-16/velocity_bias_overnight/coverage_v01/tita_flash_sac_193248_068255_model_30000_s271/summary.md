# tita_flash_sac_193248_068255_model_30000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "initial_physics_sha256": "8115e25cb8908cc43966e591043d2cacaa4756fdcf9cf657602b4f4f3c9a7a8a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0102757423613715,
  "max_drift_m": 0.017553659592398487,
  "radial_IAE_m_s": 0.6266314163222464,
  "signed_longitudinal_delta_m": 0.010275167192271428,
  "tail_speed_mean_m_s": -7.261179723080934e-06,
  "tail_speed_rms_m_s": 7.504321592325298e-06,
  "tail_sensor_speed_mean_m_s": -7.013373712943818e-06,
  "tail_fk_speed_mean_m_s": -7.313244238795035e-06,
  "peak_tilt_rad": 0.020472005493737733,
  "peak_wheel_torque_nm": 0.4120789170265198,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10924918476426271,
  "final_integral_m_s": 0.10926467935308125,
  "elapsed_wall_s": 4.302883333992213
}
```
