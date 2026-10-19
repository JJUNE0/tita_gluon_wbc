# tita_flash_sac_193248_068255_model_65000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "ad59d964fd3e68631879c59b25896b59245d01c3f316ebf079a7aa1d02869521",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016530438750561816,
  "max_drift_m": 0.033989229597278105,
  "radial_IAE_m_s": 1.074776591134742,
  "signed_longitudinal_delta_m": -0.01652077807526545,
  "tail_speed_mean_m_s": 3.430684046711721e-05,
  "tail_speed_rms_m_s": 3.4310832714627967e-05,
  "tail_sensor_speed_mean_m_s": 3.377727034514814e-05,
  "tail_fk_speed_mean_m_s": 3.518960616124997e-05,
  "peak_tilt_rad": 0.04846548381218474,
  "peak_wheel_torque_nm": 0.2336444854736328,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18793392157637254,
  "final_integral_m_s": -0.18793392157637254,
  "elapsed_wall_s": 12.05067454802338
}
```
