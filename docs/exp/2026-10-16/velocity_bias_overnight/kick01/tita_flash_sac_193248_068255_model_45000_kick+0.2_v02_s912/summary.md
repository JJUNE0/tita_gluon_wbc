# tita_flash_sac_193248_068255_model_45000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "ffbe15697a32e2108f6d358bb97a6be2bb1c3b33a0739f4d703d12329e4f5440",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018795085959977174,
  "max_drift_m": 0.03995997395424635,
  "radial_IAE_m_s": 1.1707521230153564,
  "signed_longitudinal_delta_m": -0.018791728912717375,
  "tail_speed_mean_m_s": 1.668351690895526e-05,
  "tail_speed_rms_m_s": 1.6684050171711737e-05,
  "tail_sensor_speed_mean_m_s": 1.7559516149862098e-05,
  "tail_fk_speed_mean_m_s": 1.5084608069128835e-05,
  "peak_tilt_rad": 0.084713687908482,
  "peak_wheel_torque_nm": 1.385788083076477,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.20995182819704783,
  "final_integral_m_s": -0.20998165540262548,
  "elapsed_wall_s": 14.927968470030464
}
```
