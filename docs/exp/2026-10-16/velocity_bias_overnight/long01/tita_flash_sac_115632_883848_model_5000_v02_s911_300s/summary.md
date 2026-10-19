# tita_flash_sac_115632_883848_model_5000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "22e4a8f2d12a9dc372fdc0d6564eb78b50a701268c7654595d3f9fc249c2aa35",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.042782802741506844,
  "max_drift_m": 0.08941491946601679,
  "radial_IAE_m_s": 13.56992132057627,
  "signed_longitudinal_delta_m": -0.04278177024920296,
  "tail_speed_mean_m_s": 2.0066986490256305e-05,
  "tail_speed_rms_m_s": 0.0020638123407963342,
  "tail_sensor_speed_mean_m_s": 4.161501544074677e-06,
  "tail_fk_speed_mean_m_s": 8.729017708748827e-06,
  "peak_tilt_rad": 0.1822092535706481,
  "peak_wheel_torque_nm": 3.3243772983551025,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.40936134781109634,
  "final_integral_m_s": -0.40593253148137415,
  "elapsed_wall_s": 80.65246395400027
}
```
