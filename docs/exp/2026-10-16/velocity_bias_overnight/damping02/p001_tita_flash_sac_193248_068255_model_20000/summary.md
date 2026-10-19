# p001_tita_flash_sac_193248_068255_model_20000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p001_tita_flash_sac_193248_068255_model_20000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.15,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 2.5
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
  "final_drift_m": 0.022660591202484044,
  "max_drift_m": 0.02272742747946287,
  "radial_IAE_m_s": 0.5624210089453732,
  "signed_longitudinal_delta_m": -0.022642308223142584,
  "tail_speed_mean_m_s": -0.0003614263369395366,
  "tail_speed_rms_m_s": 0.04453680587701167,
  "tail_sensor_speed_mean_m_s": -0.0004595365649380179,
  "tail_fk_speed_mean_m_s": -0.00025407152615819506,
  "peak_tilt_rad": 0.2245548055686415,
  "peak_wheel_torque_nm": 0.9598102569580078,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.32118197683614347,
  "final_integral_m_s": -0.2033180661192262,
  "elapsed_wall_s": 13.849394406017382
}
```
