# tita_flash_sac_115632_883848_model_35000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "fe14b691ca0e2c6f07d1edcfccd149a3a3a49bca81e0decc66b89a84b6f76983",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05735728942519352,
  "max_drift_m": 0.07853672682178357,
  "radial_IAE_m_s": 3.4144287803643936,
  "signed_longitudinal_delta_m": 0.057357193249491005,
  "tail_speed_mean_m_s": 1.7662228227697857e-05,
  "tail_speed_rms_m_s": 1.7834049321430307e-05,
  "tail_sensor_speed_mean_m_s": 1.7585542778849324e-05,
  "tail_fk_speed_mean_m_s": 1.9766481963155807e-05,
  "peak_tilt_rad": 0.13804581492847823,
  "peak_wheel_torque_nm": 1.2987465858459473,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6024442462683566,
  "final_integral_m_s": 0.6024100232243327,
  "elapsed_wall_s": 11.846350559033453
}
```
