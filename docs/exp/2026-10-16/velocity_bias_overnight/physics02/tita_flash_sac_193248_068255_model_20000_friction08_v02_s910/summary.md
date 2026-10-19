# tita_flash_sac_193248_068255_model_20000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "c674fdf1ee4b972ba6969b94fb5e0ca70015217d7acaca2fa1f634ab12ca1a2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06256464131461718,
  "max_drift_m": 0.08837255449066249,
  "radial_IAE_m_s": 3.8286607250732563,
  "signed_longitudinal_delta_m": 0.0625633004357135,
  "tail_speed_mean_m_s": -4.1995933796531405e-05,
  "tail_speed_rms_m_s": 4.219580282527698e-05,
  "tail_sensor_speed_mean_m_s": -2.3027432749004134e-05,
  "tail_fk_speed_mean_m_s": -1.0811784612840736e-05,
  "peak_tilt_rad": 0.14971974924805376,
  "peak_wheel_torque_nm": 1.633583426475525,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6694346219816903,
  "final_integral_m_s": 0.6694692265560831,
  "elapsed_wall_s": 19.120494367962237
}
```
