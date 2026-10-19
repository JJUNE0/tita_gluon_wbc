# tita_flash_sac_115632_883848_model_60000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "6ed5d01679f8c763956f29d0207cfec11980da29afb8fa196f3cdb9fff09bee6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.9448529710899629,
  "max_drift_m": 0.9448529710899629,
  "radial_IAE_m_s": 29.589760063357975,
  "signed_longitudinal_delta_m": 0.7239336058086472,
  "tail_speed_mean_m_s": 0.01710570406982026,
  "tail_speed_rms_m_s": 0.017105704219347293,
  "tail_sensor_speed_mean_m_s": 0.0170544684691614,
  "tail_fk_speed_mean_m_s": 0.017086243256812603,
  "peak_tilt_rad": 0.061569538574024474,
  "peak_wheel_torque_nm": 0.09812631458044052,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.918900304997806
}
```
