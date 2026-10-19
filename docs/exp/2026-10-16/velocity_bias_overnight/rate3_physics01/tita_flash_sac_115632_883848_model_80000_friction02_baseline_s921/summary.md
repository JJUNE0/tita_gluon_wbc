# tita_flash_sac_115632_883848_model_80000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "f13a88290e66d84dae03c60f55834175a759fb0191697aeb89a1872afa5e5353",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.2499007877049224,
  "max_drift_m": 4.5080890158850595,
  "radial_IAE_m_s": 193.82929641698757,
  "signed_longitudinal_delta_m": -2.174204629935813,
  "tail_speed_mean_m_s": 0.20368783490766249,
  "tail_speed_rms_m_s": 0.20368813232196606,
  "tail_sensor_speed_mean_m_s": 0.2033067752191089,
  "tail_fk_speed_mean_m_s": 0.20336559111037938,
  "peak_tilt_rad": 0.08547087142018395,
  "peak_wheel_torque_nm": 0.22654104232788086,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.475165986979846
}
```
