# tita_flash_sac_193248_068255_model_85000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "initial_physics_sha256": "24d2e5c42a1cbc99a7bc3b1a3625513668f56ff36d8733622876d07512701369",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020137687163898927,
  "max_drift_m": 0.10797591140933742,
  "radial_IAE_m_s": 1.2339752715949877,
  "signed_longitudinal_delta_m": 0.02013757968481861,
  "tail_speed_mean_m_s": 3.707205090499788e-05,
  "tail_speed_rms_m_s": 3.712096461209204e-05,
  "tail_sensor_speed_mean_m_s": 3.711039638410372e-05,
  "tail_fk_speed_mean_m_s": 3.679292102941307e-05,
  "peak_tilt_rad": 0.09894493614376176,
  "peak_wheel_torque_nm": 1.8575162887573242,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.20051658862275898,
  "final_integral_m_s": 0.2004476388832522,
  "elapsed_wall_s": 11.919885357026942
}
```
