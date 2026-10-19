# tita_flash_sac_193248_068255_model_40000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "9005d9672fcd8af06f75e65d1b14d1350fab1c7716e37f025ec54057391dd9f9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013100170496997486,
  "max_drift_m": 0.04230080555100441,
  "radial_IAE_m_s": 0.9608363669147586,
  "signed_longitudinal_delta_m": -0.01310016247752697,
  "tail_speed_mean_m_s": 7.568334272564483e-05,
  "tail_speed_rms_m_s": 7.571244061878035e-05,
  "tail_sensor_speed_mean_m_s": 7.591179311520127e-05,
  "tail_fk_speed_mean_m_s": 7.525327132460653e-05,
  "peak_tilt_rad": 0.10819185590965152,
  "peak_wheel_torque_nm": 0.8785978555679321,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2570187146082066,
  "final_integral_m_s": 0.2570187146082066,
  "elapsed_wall_s": 8.924190521996934
}
```
