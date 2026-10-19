# tita_flash_sac_115632_883848_model_40000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "92f0a7761bba368e2a0b75203122b3d174a375fe5b1b9a60a22d2e5bbcac60db",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004548947640512946,
  "max_drift_m": 0.010056272590790017,
  "radial_IAE_m_s": 0.3072096108349197,
  "signed_longitudinal_delta_m": 0.00454612817397964,
  "tail_speed_mean_m_s": -2.063328985405947e-05,
  "tail_speed_rms_m_s": 2.1369617080957037e-05,
  "tail_sensor_speed_mean_m_s": -2.0532934413484155e-05,
  "tail_fk_speed_mean_m_s": -2.0104129848163213e-05,
  "peak_tilt_rad": 0.11285101630404393,
  "peak_wheel_torque_nm": 0.38937246799468994,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03699895013778056,
  "final_integral_m_s": -0.03699895013778056,
  "elapsed_wall_s": 12.559706613013986
}
```
