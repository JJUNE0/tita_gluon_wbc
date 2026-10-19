# tita_flash_sac_193248_068255_model_85000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 7.149977925951004,
  "max_drift_m": 7.149977925951004,
  "radial_IAE_m_s": 215.4328234871695,
  "signed_longitudinal_delta_m": 7.147309784316044,
  "tail_speed_mean_m_s": 0.12019238084721831,
  "tail_speed_rms_m_s": 0.12019370465605775,
  "tail_sensor_speed_mean_m_s": 0.11989473340540853,
  "tail_fk_speed_mean_m_s": 0.11992904471324156,
  "peak_tilt_rad": 0.07542653589608461,
  "peak_wheel_torque_nm": 1.3732980489730835,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.361581615987234
}
```
