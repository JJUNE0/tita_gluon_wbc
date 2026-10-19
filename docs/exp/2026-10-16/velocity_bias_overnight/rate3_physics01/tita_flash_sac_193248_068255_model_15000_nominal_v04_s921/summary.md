# tita_flash_sac_193248_068255_model_15000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "initial_physics_sha256": "0dacc359635104403574016f58cbbaec66e8c59e8929a4243976305907524fa5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0010196859980820712,
  "max_drift_m": 0.02385156427431273,
  "radial_IAE_m_s": 0.06893902700700694,
  "signed_longitudinal_delta_m": -0.0009833660433953648,
  "tail_speed_mean_m_s": -1.1180055349930581e-05,
  "tail_speed_rms_m_s": 1.1184822765546806e-05,
  "tail_sensor_speed_mean_m_s": -1.1243317804766387e-05,
  "tail_fk_speed_mean_m_s": -8.93401847885778e-06,
  "peak_tilt_rad": 0.0953681933429602,
  "peak_wheel_torque_nm": 0.4803476929664612,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18243547705664012,
  "final_integral_m_s": -0.18243547705664012,
  "elapsed_wall_s": 7.387346572009847
}
```
