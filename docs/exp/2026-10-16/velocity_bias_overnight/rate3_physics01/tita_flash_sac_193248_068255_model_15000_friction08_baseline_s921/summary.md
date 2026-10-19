# tita_flash_sac_193248_068255_model_15000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "6928f6feac9aa42b24ec1fc590b1dbfd78ab2cfc24492804a87d6aedb2d4f485",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.376943062224466,
  "max_drift_m": 3.376943062224466,
  "radial_IAE_m_s": 101.54942113528705,
  "signed_longitudinal_delta_m": -3.3766338010834116,
  "tail_speed_mean_m_s": -0.055978293862280516,
  "tail_speed_rms_m_s": 0.055978443022010764,
  "tail_sensor_speed_mean_m_s": -0.05588956095559365,
  "tail_fk_speed_mean_m_s": -0.0558915011517983,
  "peak_tilt_rad": 0.04462923850920997,
  "peak_wheel_torque_nm": 0.08554717898368835,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.800743684987538
}
```
