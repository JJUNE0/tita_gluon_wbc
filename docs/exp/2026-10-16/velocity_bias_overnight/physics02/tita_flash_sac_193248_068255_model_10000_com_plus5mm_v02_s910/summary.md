# tita_flash_sac_193248_068255_model_10000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "e31e4f28a0e7407b6fad2c3bf501657f1185f2ccee9e7d1a9f03458323901aac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024272560404468208,
  "max_drift_m": 0.024272560404468208,
  "radial_IAE_m_s": 1.3326086850816579,
  "signed_longitudinal_delta_m": 0.024209912128612593,
  "tail_speed_mean_m_s": 4.684912502825974e-05,
  "tail_speed_rms_m_s": 4.697075764622938e-05,
  "tail_sensor_speed_mean_m_s": 6.237220140610363e-05,
  "tail_fk_speed_mean_m_s": 6.934483198607749e-05,
  "peak_tilt_rad": 0.025824841471627044,
  "peak_wheel_torque_nm": 0.8670332431793213,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2580340182859002,
  "final_integral_m_s": 0.25788159603773686,
  "elapsed_wall_s": 16.805443366989493
}
```
