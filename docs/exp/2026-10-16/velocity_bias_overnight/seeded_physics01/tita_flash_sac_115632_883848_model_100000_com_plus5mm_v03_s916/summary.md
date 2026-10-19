# tita_flash_sac_115632_883848_model_100000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "b406d6c7d646a56ffb05247cd7f1afbfb47c462643ad8ff720d906c68b76a4fb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09415821851337194,
  "max_drift_m": 0.12326463730470782,
  "radial_IAE_m_s": 5.543261398333559,
  "signed_longitudinal_delta_m": 0.09415775368298616,
  "tail_speed_mean_m_s": 5.037920685853456e-05,
  "tail_speed_rms_m_s": 5.125306567787624e-05,
  "tail_sensor_speed_mean_m_s": 5.017615969084028e-05,
  "tail_fk_speed_mean_m_s": 4.9977999030939456e-05,
  "peak_tilt_rad": 0.08501626697894671,
  "peak_wheel_torque_nm": 0.6516899466514587,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6043017851783377,
  "final_integral_m_s": 0.6043017851783377,
  "elapsed_wall_s": 19.05006547900848
}
```
