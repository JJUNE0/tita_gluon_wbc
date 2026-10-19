# tita_flash_sac_115632_883848_model_10000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "d7556c4271eeee87de3e5e7a7140859699c494f176c7a1c2ffd2e8bd1d30faf3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017236883217144332,
  "max_drift_m": 0.029654358981391554,
  "radial_IAE_m_s": 0.873508609000119,
  "signed_longitudinal_delta_m": 0.017133111604616603,
  "tail_speed_mean_m_s": 8.840364337387393e-05,
  "tail_speed_rms_m_s": 8.842102892697566e-05,
  "tail_sensor_speed_mean_m_s": 8.825352673188203e-05,
  "tail_fk_speed_mean_m_s": 8.787269400360563e-05,
  "peak_tilt_rad": 0.12494680479168574,
  "peak_wheel_torque_nm": 2.3530189990997314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15007221849662325,
  "final_integral_m_s": -0.15007221849662325,
  "elapsed_wall_s": 10.238976166001521
}
```
