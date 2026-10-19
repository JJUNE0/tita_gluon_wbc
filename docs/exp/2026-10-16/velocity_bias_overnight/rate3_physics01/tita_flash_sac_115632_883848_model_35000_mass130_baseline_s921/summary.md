# tita_flash_sac_115632_883848_model_35000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "db4fe87ec0ed5a75c397623f1f405c2f452e52fbb635a40829bb4e298e4189fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.1593610590266519,
  "max_drift_m": 1.1593610590266519,
  "radial_IAE_m_s": 33.81030671321643,
  "signed_longitudinal_delta_m": 1.158644797330264,
  "tail_speed_mean_m_s": 0.020321100144813357,
  "tail_speed_rms_m_s": 0.02032253557581609,
  "tail_sensor_speed_mean_m_s": 0.020277438816953146,
  "tail_fk_speed_mean_m_s": 0.020277662956943252,
  "peak_tilt_rad": 0.12207659637219948,
  "peak_wheel_torque_nm": 0.7106031179428101,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.616129495960195
}
```
