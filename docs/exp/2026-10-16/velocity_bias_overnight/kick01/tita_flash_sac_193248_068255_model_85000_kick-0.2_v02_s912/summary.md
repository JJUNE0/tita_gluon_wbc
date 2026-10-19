# tita_flash_sac_193248_068255_model_85000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "079e3d4eb197d4f613f809616455dc7d9186f54a8ef806877b4b53af65dbb08f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017180853105857895,
  "max_drift_m": 0.05657476511679158,
  "radial_IAE_m_s": 0.9875719497832836,
  "signed_longitudinal_delta_m": 0.017180844641655608,
  "tail_speed_mean_m_s": 3.972746895039014e-05,
  "tail_speed_rms_m_s": 3.97659720561289e-05,
  "tail_sensor_speed_mean_m_s": 3.975995247555991e-05,
  "tail_fk_speed_mean_m_s": 3.946159275142777e-05,
  "peak_tilt_rad": 0.0695207033549965,
  "peak_wheel_torque_nm": 1.692514419555664,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19744282857710954,
  "final_integral_m_s": 0.19737441873381137,
  "elapsed_wall_s": 11.551994006964378
}
```
