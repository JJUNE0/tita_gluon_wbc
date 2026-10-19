# tita_flash_sac_193248_068255_model_50000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "3b4f0c72436a68a0dac951af1c44b9acc40dc2a85ec5169a0f8670d53f4176b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07035640828111431,
  "max_drift_m": 0.10493080275046032,
  "radial_IAE_m_s": 4.222382578468681,
  "signed_longitudinal_delta_m": 0.07035331253069149,
  "tail_speed_mean_m_s": 2.009603233519717e-05,
  "tail_speed_rms_m_s": 2.0122496659586892e-05,
  "tail_sensor_speed_mean_m_s": 2.0041563153111953e-05,
  "tail_fk_speed_mean_m_s": 2.1045440539390584e-05,
  "peak_tilt_rad": 0.08343423578249687,
  "peak_wheel_torque_nm": 2.076169013977051,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7050835628511384,
  "final_integral_m_s": 0.7050530030500103,
  "elapsed_wall_s": 14.097423460974824
}
```
