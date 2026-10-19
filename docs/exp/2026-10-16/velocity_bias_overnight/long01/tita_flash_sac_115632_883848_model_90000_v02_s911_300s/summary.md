# tita_flash_sac_115632_883848_model_90000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "d874b4d8724ad32d4f2482059492e6e5f97ee21710c1e58e5d337f12fff3ea7f",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.04873625134592294,
  "max_drift_m": 0.04873625134592294,
  "radial_IAE_m_s": 12.79981891297363,
  "signed_longitudinal_delta_m": 0.048715826889995165,
  "tail_speed_mean_m_s": 3.145815512797002e-05,
  "tail_speed_rms_m_s": 3.160253645709737e-05,
  "tail_sensor_speed_mean_m_s": 3.2791949145418936e-05,
  "tail_fk_speed_mean_m_s": 3.478596904045676e-05,
  "peak_tilt_rad": 0.06904601730503557,
  "peak_wheel_torque_nm": 0.4829440712928772,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4978217271386892,
  "final_integral_m_s": 0.4977584864438767,
  "elapsed_wall_s": 69.20606982999016
}
```
