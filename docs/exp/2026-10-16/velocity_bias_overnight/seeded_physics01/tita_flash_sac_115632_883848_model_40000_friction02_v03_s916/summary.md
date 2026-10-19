# tita_flash_sac_115632_883848_model_40000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "baa210e664677078ddef8a5c884f2aac138a6d83f9628912c74385fe24461b89",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.015083208004213923,
  "max_drift_m": 0.038622329195183366,
  "radial_IAE_m_s": 0.952097195384845,
  "signed_longitudinal_delta_m": -0.008869842399170845,
  "tail_speed_mean_m_s": -0.00011002238357169257,
  "tail_speed_rms_m_s": 0.00011002244257695836,
  "tail_sensor_speed_mean_m_s": -3.0972106993653664e-05,
  "tail_fk_speed_mean_m_s": -3.2726305143877385e-07,
  "peak_tilt_rad": 0.10849958243063007,
  "peak_wheel_torque_nm": 0.8821187615394592,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2166648347668421,
  "final_integral_m_s": 0.2166648347668421,
  "elapsed_wall_s": 11.94919780199416
}
```
