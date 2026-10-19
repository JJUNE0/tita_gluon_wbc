# tita_flash_sac_193248_068255_model_70000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "aa6879f87b5b02b8cea1ac725358ec03ea6a15a3a2909e99b37d8062ceed4dcc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.575282115573369,
  "max_drift_m": 5.575282115573369,
  "radial_IAE_m_s": 159.26071489648143,
  "signed_longitudinal_delta_m": 5.573545209678936,
  "tail_speed_mean_m_s": 0.10000796708339504,
  "tail_speed_rms_m_s": 0.10000815281958443,
  "tail_sensor_speed_mean_m_s": 0.09979187072962047,
  "tail_fk_speed_mean_m_s": 0.09979082876800748,
  "peak_tilt_rad": 0.09063869250506329,
  "peak_wheel_torque_nm": 0.08578003942966461,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.704314555972815
}
```
