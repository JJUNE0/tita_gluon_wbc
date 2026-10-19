# tita_flash_sac_115632_883848_model_90000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "52ed719826815c3906b2fd95a44df11b9b48d555ed06bf7d7d9df6838eecb989",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.07130270350051669,
  "max_drift_m": 0.07130270350051669,
  "radial_IAE_m_s": 16.762863988534797,
  "signed_longitudinal_delta_m": 0.07122333500251492,
  "tail_speed_mean_m_s": 8.488336762343283e-05,
  "tail_speed_rms_m_s": 8.505888806782444e-05,
  "tail_sensor_speed_mean_m_s": 8.596275863609039e-05,
  "tail_fk_speed_mean_m_s": 8.791338865211326e-05,
  "peak_tilt_rad": 0.06916747433291959,
  "peak_wheel_torque_nm": 0.41307148337364197,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.49704839419472513,
  "final_integral_m_s": 0.49704839419472513,
  "elapsed_wall_s": 47.68464639503509
}
```
