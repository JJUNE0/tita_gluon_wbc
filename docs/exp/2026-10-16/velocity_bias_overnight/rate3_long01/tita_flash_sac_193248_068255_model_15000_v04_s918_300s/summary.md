# tita_flash_sac_193248_068255_model_15000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "initial_physics_sha256": "c80e9569675d5c84dd0f32360724a83de26ec076f251ebb8f145e54acd2934d5",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0041077154889481516,
  "max_drift_m": 0.02385159460035074,
  "radial_IAE_m_s": 0.6756817313692193,
  "signed_longitudinal_delta_m": -0.0041011267002010856,
  "tail_speed_mean_m_s": -1.2343741013566946e-05,
  "tail_speed_rms_m_s": 1.23492671564907e-05,
  "tail_sensor_speed_mean_m_s": -1.1836072812085191e-05,
  "tail_fk_speed_mean_m_s": -9.372026761439406e-06,
  "peak_tilt_rad": 0.09536834320557963,
  "peak_wheel_torque_nm": 0.4803376793861389,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19211179463322642,
  "final_integral_m_s": -0.19211179463322642,
  "elapsed_wall_s": 51.47211017902009
}
```
