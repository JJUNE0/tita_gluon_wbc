# tita_flash_sac_115632_883848_model_35000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_s271",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "e62d0332d89b35c67ef891d7dd3ee42dbdb39adaac22d10c2a375db21c7fa2f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05746689531625565,
  "max_drift_m": 0.1025709985400453,
  "radial_IAE_m_s": 3.468267641778132,
  "signed_longitudinal_delta_m": 0.057466182083520397,
  "tail_speed_mean_m_s": 3.286627131430376e-06,
  "tail_speed_rms_m_s": 4.910955996577808e-06,
  "tail_sensor_speed_mean_m_s": 3.2801920043958966e-06,
  "tail_fk_speed_mean_m_s": 5.240794594036205e-06,
  "peak_tilt_rad": 0.13847770763121225,
  "peak_wheel_torque_nm": 1.3369097709655762,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6055831825056371,
  "final_integral_m_s": 0.6055488876718249,
  "elapsed_wall_s": 4.401169418008067
}
```
