# tita_flash_sac_115632_883848_model_35000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "final_drift_m": 0.0573396275365434,
  "max_drift_m": 0.08303782822358904,
  "radial_IAE_m_s": 3.4148048791627317,
  "signed_longitudinal_delta_m": 0.05733954449165815,
  "tail_speed_mean_m_s": 1.7827212895511334e-05,
  "tail_speed_rms_m_s": 1.8001150677777678e-05,
  "tail_sensor_speed_mean_m_s": 1.773869066543205e-05,
  "tail_fk_speed_mean_m_s": 1.9932090113173716e-05,
  "peak_tilt_rad": 0.1385877135655107,
  "peak_wheel_torque_nm": 1.2029550075531006,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.60229172111624,
  "final_integral_m_s": 0.6022571715361257,
  "elapsed_wall_s": 5.97521180997137
}
```
