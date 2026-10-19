# tita_flash_sac_193248_068255_model_95000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "initial_physics_sha256": "6661f5839098126b9b6417b6e338eedc9f81d6081db34ffbe57205a83a133f18",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.014574686351528537,
  "max_drift_m": 0.084722693642724,
  "radial_IAE_m_s": 4.43318979256912,
  "signed_longitudinal_delta_m": 0.014574685008470934,
  "tail_speed_mean_m_s": 4.000285424621341e-06,
  "tail_speed_rms_m_s": 4.001462985659739e-06,
  "tail_sensor_speed_mean_m_s": 4.128680347579785e-06,
  "tail_fk_speed_mean_m_s": 3.528635301155271e-06,
  "peak_tilt_rad": 0.08476502622797066,
  "peak_wheel_torque_nm": 0.5866304636001587,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23343994994576464,
  "final_integral_m_s": -0.23343994994576464,
  "elapsed_wall_s": 26.628140518034343
}
```
