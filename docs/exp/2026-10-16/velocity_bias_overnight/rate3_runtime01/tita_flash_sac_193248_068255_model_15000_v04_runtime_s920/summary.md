# tita_flash_sac_193248_068255_model_15000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "initial_physics_sha256": "b87a9f9ba352e6bd6162703d46c679addffa30512ad77d56ccd7acec3442b1c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0008820620776120508,
  "max_drift_m": 0.023905578070537913,
  "radial_IAE_m_s": 0.06285183092718725,
  "signed_longitudinal_delta_m": -0.0008389935553269147,
  "tail_speed_mean_m_s": -1.1105351627054252e-05,
  "tail_speed_rms_m_s": 1.1108186954240654e-05,
  "tail_sensor_speed_mean_m_s": -1.1281226683088378e-05,
  "tail_fk_speed_mean_m_s": -8.967457819088245e-06,
  "peak_tilt_rad": 0.09556956939092598,
  "peak_wheel_torque_nm": 0.4829462170600891,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18253865369874506,
  "final_integral_m_s": -0.18253865369874506,
  "elapsed_wall_s": 12.83875466499012
}
```
