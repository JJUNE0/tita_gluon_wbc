# tita_flash_sac_193248_068255_model_15000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "initial_physics_sha256": "a84217f9d9dd6b08d089a33248572d921d9e0406d6bdfd548ad7c32a845d2300",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03363871111986347,
  "max_drift_m": 0.042517729037016866,
  "radial_IAE_m_s": 2.196401375183174,
  "signed_longitudinal_delta_m": -0.03360120525765154,
  "tail_speed_mean_m_s": 4.97157367089509e-05,
  "tail_speed_rms_m_s": 0.01903517152651687,
  "tail_sensor_speed_mean_m_s": 0.0016063500478261993,
  "tail_fk_speed_mean_m_s": 7.085632330416934e-05,
  "peak_tilt_rad": 0.17337692272417948,
  "peak_wheel_torque_nm": 4.477084159851074,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3316845869295979,
  "final_integral_m_s": -0.3316845869295979,
  "elapsed_wall_s": 8.74312908097636
}
```
