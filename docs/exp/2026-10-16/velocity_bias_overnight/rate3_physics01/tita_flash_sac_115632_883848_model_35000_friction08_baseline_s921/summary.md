# tita_flash_sac_115632_883848_model_35000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "5bfb7f1d3dee33c2bceacc8f8713d3023f5aa6c4117a2dc6730d0e2510fe6770",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.762184879815281,
  "max_drift_m": 13.762184879815281,
  "radial_IAE_m_s": 408.6632097158931,
  "signed_longitudinal_delta_m": 13.759302961814084,
  "tail_speed_mean_m_s": 0.23247895188266712,
  "tail_speed_rms_m_s": 0.23247895535783072,
  "tail_sensor_speed_mean_m_s": 0.2319760404091222,
  "tail_fk_speed_mean_m_s": 0.2319741033712524,
  "peak_tilt_rad": 0.14077214676689076,
  "peak_wheel_torque_nm": 0.9021536111831665,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.298799728043377
}
```
