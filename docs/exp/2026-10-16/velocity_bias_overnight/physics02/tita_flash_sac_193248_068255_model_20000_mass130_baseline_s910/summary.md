# tita_flash_sac_193248_068255_model_20000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "bb5de423d1bc5b38f9ad5544f877dc8ad7f955fb02a7c2ae6b556258a14811e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.7888917609010493,
  "max_drift_m": 2.7888917609010493,
  "radial_IAE_m_s": 83.05108707627981,
  "signed_longitudinal_delta_m": -2.786213338182911,
  "tail_speed_mean_m_s": -0.047060306356343305,
  "tail_speed_rms_m_s": 0.047060476088941955,
  "tail_sensor_speed_mean_m_s": -0.0469601057539197,
  "tail_fk_speed_mean_m_s": -0.046958242609967324,
  "peak_tilt_rad": 0.12389028341130226,
  "peak_wheel_torque_nm": 0.2751949727535248,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.083222955989186
}
```
