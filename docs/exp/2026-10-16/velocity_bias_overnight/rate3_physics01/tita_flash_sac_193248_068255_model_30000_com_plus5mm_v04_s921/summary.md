# tita_flash_sac_193248_068255_model_30000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "aabaae75f6dc8f204ea6ac5821e17bde5145e6ad880ad5f4eda72d46093d069d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015998470608763516,
  "max_drift_m": 0.024682836237101005,
  "radial_IAE_m_s": 0.942665484551475,
  "signed_longitudinal_delta_m": -0.015992541274379178,
  "tail_speed_mean_m_s": -1.6724178143906386e-05,
  "tail_speed_rms_m_s": 1.6730286578495557e-05,
  "tail_sensor_speed_mean_m_s": -1.6484682915005494e-05,
  "tail_fk_speed_mean_m_s": -1.668588427983597e-05,
  "peak_tilt_rad": 0.03414357082252084,
  "peak_wheel_torque_nm": 0.5346388816833496,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.148229397210445,
  "final_integral_m_s": 0.148229397210445,
  "elapsed_wall_s": 8.707670080999378
}
```
