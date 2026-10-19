# tita_flash_sac_193248_068255_model_20000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "2f01feda273036b4a10e3a969c0318e094cf64c9501a9857c6f2de2cae2529dd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014988061596982072,
  "max_drift_m": 0.027284720419950944,
  "radial_IAE_m_s": 0.9047261829731708,
  "signed_longitudinal_delta_m": -0.01498054640407161,
  "tail_speed_mean_m_s": 1.320761081268329e-06,
  "tail_speed_rms_m_s": 1.351046704764751e-06,
  "tail_sensor_speed_mean_m_s": 1.215121872237667e-06,
  "tail_fk_speed_mean_m_s": 4.011411465133136e-06,
  "peak_tilt_rad": 0.14351457764465292,
  "peak_wheel_torque_nm": 1.0958960056304932,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16263961877441147,
  "final_integral_m_s": 0.16263961877441147,
  "elapsed_wall_s": 9.048231093969662
}
```
