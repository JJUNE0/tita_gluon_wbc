# tita_flash_sac_193248_068255_model_75000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "45add98c66d87597f0623533321114a1eeda90d086602ed510df897a279cf27b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.470405601026538,
  "max_drift_m": 15.470405601026538,
  "radial_IAE_m_s": 477.97651021281405,
  "signed_longitudinal_delta_m": -14.044849450030465,
  "tail_speed_mean_m_s": -0.29946967947771475,
  "tail_speed_rms_m_s": 0.29956835508807755,
  "tail_sensor_speed_mean_m_s": -0.2987176025629897,
  "tail_fk_speed_mean_m_s": -0.29874148497226755,
  "peak_tilt_rad": 0.08562666590632007,
  "peak_wheel_torque_nm": 0.6799244284629822,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.977102798002306
}
```
