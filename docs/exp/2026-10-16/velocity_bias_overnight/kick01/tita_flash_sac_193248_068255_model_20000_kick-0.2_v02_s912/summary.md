# tita_flash_sac_193248_068255_model_20000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "1ec06f932cb130c1bd860eaf26cbde5845728a6087f175f27a7e1c98391bf687",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.062049607100139036,
  "max_drift_m": 0.0641792396800321,
  "radial_IAE_m_s": 3.738627652082116,
  "signed_longitudinal_delta_m": 0.06204960681151539,
  "tail_speed_mean_m_s": -3.178123502751729e-05,
  "tail_speed_rms_m_s": 3.178455472546133e-05,
  "tail_sensor_speed_mean_m_s": -1.5631971813595572e-05,
  "tail_fk_speed_mean_m_s": -5.607093759743853e-06,
  "peak_tilt_rad": 0.1464870334185142,
  "peak_wheel_torque_nm": 1.5344727039337158,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6787883064634173,
  "final_integral_m_s": 0.6787996439781824,
  "elapsed_wall_s": 13.749982620996889
}
```
