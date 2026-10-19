# tita_flash_sac_115632_883848_model_35000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
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
  "initial_physics_sha256": "7045fdedd39f6724cabf4544c66cc164a6ed4e4ebaf93c70091a0bec8c312bd7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.052574387885107314,
  "max_drift_m": 0.06885334394541803,
  "radial_IAE_m_s": 3.1422254768350744,
  "signed_longitudinal_delta_m": 0.05257240252431312,
  "tail_speed_mean_m_s": 3.6047863414696714e-06,
  "tail_speed_rms_m_s": 3.714415201520573e-06,
  "tail_sensor_speed_mean_m_s": 3.477812691066345e-06,
  "tail_fk_speed_mean_m_s": 5.777974259028973e-06,
  "peak_tilt_rad": 0.13620471771424647,
  "peak_wheel_torque_nm": 1.351546287536621,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5539336916163218,
  "final_integral_m_s": 0.5539131622753283,
  "elapsed_wall_s": 12.440300548973028
}
```
