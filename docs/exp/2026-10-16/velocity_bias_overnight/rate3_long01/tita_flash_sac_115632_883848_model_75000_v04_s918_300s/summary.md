# tita_flash_sac_115632_883848_model_75000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "6366aad38c3f71b70b0d14f6ff0d7398d51fb21b6fb83762cb9999959ce9bb17",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.047622889124775,
  "max_drift_m": 0.05044031096403437,
  "radial_IAE_m_s": 12.568238396835042,
  "signed_longitudinal_delta_m": 0.04757278207991083,
  "tail_speed_mean_m_s": 3.732846580813933e-05,
  "tail_speed_rms_m_s": 3.7330255397587603e-05,
  "tail_sensor_speed_mean_m_s": 3.717474919254196e-05,
  "tail_fk_speed_mean_m_s": 3.774347075523923e-05,
  "peak_tilt_rad": 0.06732098520076701,
  "peak_wheel_torque_nm": 0.3630789518356323,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04138332967360825,
  "final_integral_m_s": 0.04138332967360825,
  "elapsed_wall_s": 49.04673714097589
}
```
