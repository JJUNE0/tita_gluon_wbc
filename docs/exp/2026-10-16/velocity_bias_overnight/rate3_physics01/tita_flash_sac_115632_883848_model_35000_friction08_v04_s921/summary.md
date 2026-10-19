# tita_flash_sac_115632_883848_model_35000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.026204594124588892,
  "max_drift_m": 0.07036162164387498,
  "radial_IAE_m_s": 1.5162866636729206,
  "signed_longitudinal_delta_m": 0.02620452691023804,
  "tail_speed_mean_m_s": 4.645551203606377e-05,
  "tail_speed_rms_m_s": 4.69094760366661e-05,
  "tail_sensor_speed_mean_m_s": 4.60806810917797e-05,
  "tail_fk_speed_mean_m_s": 4.849166586545832e-05,
  "peak_tilt_rad": 0.13707870389525523,
  "peak_wheel_torque_nm": 2.3143508434295654,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5995668371713992,
  "final_integral_m_s": 0.5995668371713992,
  "elapsed_wall_s": 10.989050119009335
}
```
