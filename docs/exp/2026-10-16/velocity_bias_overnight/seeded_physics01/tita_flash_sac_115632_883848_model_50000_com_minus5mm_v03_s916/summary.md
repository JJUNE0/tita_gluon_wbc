# tita_flash_sac_115632_883848_model_50000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "bc6b350abfa161dcf4bc5026f9ffff4954570ef32bd87984b232678b343b95ae",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0037276705972444212,
  "max_drift_m": 0.005260681180153259,
  "radial_IAE_m_s": 0.21193070165229733,
  "signed_longitudinal_delta_m": 0.0028127205116347835,
  "tail_speed_mean_m_s": -1.3242906806226605e-06,
  "tail_speed_rms_m_s": 2.342236813405588e-06,
  "tail_sensor_speed_mean_m_s": -1.2069997233365982e-06,
  "tail_fk_speed_mean_m_s": 1.3214969112942818e-06,
  "peak_tilt_rad": 0.04295398204666401,
  "peak_wheel_torque_nm": 0.28879210352897644,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.018139607085191675,
  "final_integral_m_s": -0.018139607085191675,
  "elapsed_wall_s": 12.028312779963017
}
```
