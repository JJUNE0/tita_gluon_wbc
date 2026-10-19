# tita_flash_sac_193248_068255_model_95000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "2e4b78a84e35bc3698458065547b664ea03339fb521367a6642c0bb41f949b8d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013583240080728785,
  "max_drift_m": 0.08473883954110288,
  "radial_IAE_m_s": 1.058825762796494,
  "signed_longitudinal_delta_m": 0.013578873112714591,
  "tail_speed_mean_m_s": 3.1139932684044204e-06,
  "tail_speed_rms_m_s": 2.0521152620933275e-05,
  "tail_sensor_speed_mean_m_s": 3.4062223398546113e-06,
  "tail_fk_speed_mean_m_s": 2.750655678656456e-06,
  "peak_tilt_rad": 0.08476934357065957,
  "peak_wheel_torque_nm": 0.5855390429496765,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23719568163136448,
  "final_integral_m_s": -0.23719568163136448,
  "elapsed_wall_s": 8.882759567990433
}
```
