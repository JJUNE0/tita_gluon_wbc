# tita_flash_sac_193248_068255_model_10000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "d58e5460ddd6c38d7935de3c226dd71f1764ba013af8c5e5c3efc0a993c4acf1",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.04706990034426945,
  "max_drift_m": 0.04706990034426945,
  "radial_IAE_m_s": 9.338137844017545,
  "signed_longitudinal_delta_m": 0.04129622297622283,
  "tail_speed_mean_m_s": 8.793499260232675e-05,
  "tail_speed_rms_m_s": 8.795205494114139e-05,
  "tail_sensor_speed_mean_m_s": 8.909876765800581e-05,
  "tail_fk_speed_mean_m_s": 9.343960786972306e-05,
  "peak_tilt_rad": 0.027324750593431757,
  "peak_wheel_torque_nm": 0.8904516696929932,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2363672096414728,
  "final_integral_m_s": 0.2363672096414728,
  "elapsed_wall_s": 45.09993912698701
}
```
