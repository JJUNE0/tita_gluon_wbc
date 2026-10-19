# tita_flash_sac_193248_068255_model_10000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "f8b260c29be8e666b45c3bcb76e9ad42fa6da6616e7771ddcdc955d5aebd5187",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.048919262324724336,
  "max_drift_m": 0.05003675629382638,
  "radial_IAE_m_s": 2.937099724930681,
  "signed_longitudinal_delta_m": -0.048919260293561216,
  "tail_speed_mean_m_s": 2.1275445053779853e-05,
  "tail_speed_rms_m_s": 2.1277777872098575e-05,
  "tail_sensor_speed_mean_m_s": 2.217934874796767e-05,
  "tail_fk_speed_mean_m_s": 2.3940210792382225e-05,
  "peak_tilt_rad": 0.0940601864744195,
  "peak_wheel_torque_nm": 1.1510951519012451,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4968906538366775,
  "final_integral_m_s": -0.49693746061248134,
  "elapsed_wall_s": 17.87788072001422
}
```
