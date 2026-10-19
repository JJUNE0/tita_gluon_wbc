# tita_flash_sac_193248_068255_model_95000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "68e0c769d3f3a7977fc54a52f30206beb3c9541a189be3c319992fa614c81bf7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03460836417211142,
  "max_drift_m": 0.07693684043567364,
  "radial_IAE_m_s": 2.0813653093829476,
  "signed_longitudinal_delta_m": -0.03460599650669085,
  "tail_speed_mean_m_s": -3.975306427209755e-06,
  "tail_speed_rms_m_s": 3.9765769699613154e-06,
  "tail_sensor_speed_mean_m_s": -3.978933021418647e-06,
  "tail_fk_speed_mean_m_s": -3.824659769093031e-06,
  "peak_tilt_rad": 0.12949497782055364,
  "peak_wheel_torque_nm": 1.0164177417755127,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3654456393562858,
  "final_integral_m_s": -0.36543834256181845,
  "elapsed_wall_s": 18.62767256097868
}
```
