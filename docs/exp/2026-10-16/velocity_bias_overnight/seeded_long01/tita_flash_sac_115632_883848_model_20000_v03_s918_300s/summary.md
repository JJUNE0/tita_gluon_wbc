# tita_flash_sac_115632_883848_model_20000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "76e3ee49bb2a73977ec541d378239579ec194398c4465b12e7f5b6e51b76770d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.03029750284646746,
  "max_drift_m": 0.09994768473884355,
  "radial_IAE_m_s": 8.977230798067433,
  "signed_longitudinal_delta_m": -0.028422360922743556,
  "tail_speed_mean_m_s": 3.0020063041462594e-05,
  "tail_speed_rms_m_s": 3.099717608499485e-05,
  "tail_sensor_speed_mean_m_s": -0.0001480672670438675,
  "tail_fk_speed_mean_m_s": 1.140296783037876e-06,
  "peak_tilt_rad": 0.15296564998124884,
  "peak_wheel_torque_nm": 0.8768228888511658,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3843665121619161,
  "final_integral_m_s": 0.3843665121619161,
  "elapsed_wall_s": 53.26785852498142
}
```
