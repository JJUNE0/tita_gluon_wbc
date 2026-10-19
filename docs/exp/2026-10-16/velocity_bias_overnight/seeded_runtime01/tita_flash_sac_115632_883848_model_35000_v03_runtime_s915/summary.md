# tita_flash_sac_115632_883848_model_35000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "83d70512782d9772a60746c8c117f8a2accb74e8c18b33abe4fc7df84910b492",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024236563253148297,
  "max_drift_m": 0.07764857416117449,
  "radial_IAE_m_s": 1.4368228248101391,
  "signed_longitudinal_delta_m": 0.0242364364130852,
  "tail_speed_mean_m_s": 4.049258612064006e-05,
  "tail_speed_rms_m_s": 4.163285826054041e-05,
  "tail_sensor_speed_mean_m_s": 4.038897364979483e-05,
  "tail_fk_speed_mean_m_s": 4.2545706671736116e-05,
  "peak_tilt_rad": 0.13718915524094255,
  "peak_wheel_torque_nm": 1.393632173538208,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6029339031944345,
  "final_integral_m_s": 0.6029339031944345,
  "elapsed_wall_s": 16.864549353020266
}
```
