# tita_flash_sac_115632_883848_model_35000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "e16811a5ec7586098174f1f118fcddaa8a0c4215d53180d6667d26daa34db4e5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.057338625310622005,
  "max_drift_m": 0.07840195743936382,
  "radial_IAE_m_s": 3.4128208262906226,
  "signed_longitudinal_delta_m": 0.05733851259509599,
  "tail_speed_mean_m_s": 1.7850079186267115e-05,
  "tail_speed_rms_m_s": 1.801525368020906e-05,
  "tail_sensor_speed_mean_m_s": 1.7758981366635862e-05,
  "tail_fk_speed_mean_m_s": 1.9955214015326848e-05,
  "peak_tilt_rad": 0.13806318922374028,
  "peak_wheel_torque_nm": 1.2992534637451172,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6022581764254449,
  "final_integral_m_s": 0.6022235415067347,
  "elapsed_wall_s": 5.7878192490316
}
```
