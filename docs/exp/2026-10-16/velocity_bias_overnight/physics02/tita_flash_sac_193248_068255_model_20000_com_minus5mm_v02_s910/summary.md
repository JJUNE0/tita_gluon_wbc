# tita_flash_sac_193248_068255_model_20000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "initial_physics_sha256": "80afd21098615a31ac96e6a608b4d4f12bf9ab804e00f6474b82e0771cc3578f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.061877726901675485,
  "max_drift_m": 0.08175136579699308,
  "radial_IAE_m_s": 3.777325121985858,
  "signed_longitudinal_delta_m": 0.061876447058945294,
  "tail_speed_mean_m_s": -3.616759737510432e-05,
  "tail_speed_rms_m_s": 3.6173168759712646e-05,
  "tail_sensor_speed_mean_m_s": -1.7471735447744875e-05,
  "tail_fk_speed_mean_m_s": -5.600793734845442e-06,
  "peak_tilt_rad": 0.1442908654188304,
  "peak_wheel_torque_nm": 1.655847191810608,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6616824630034882,
  "final_integral_m_s": 0.661694047887815,
  "elapsed_wall_s": 21.679713456018362
}
```
