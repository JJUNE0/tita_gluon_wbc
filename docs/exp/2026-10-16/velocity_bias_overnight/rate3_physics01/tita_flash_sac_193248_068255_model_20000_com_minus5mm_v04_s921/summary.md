# tita_flash_sac_193248_068255_model_20000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "5eeeb4fee4c6e636fbbaed5fc1b056ee265b3211d9b907cdac9413140fc6ca2d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020984873156329232,
  "max_drift_m": 0.07031517031071148,
  "radial_IAE_m_s": 1.4014297903847432,
  "signed_longitudinal_delta_m": 0.020984855829052632,
  "tail_speed_mean_m_s": -4.479098821562659e-05,
  "tail_speed_rms_m_s": 4.479865600269336e-05,
  "tail_sensor_speed_mean_m_s": -2.597953983527608e-05,
  "tail_fk_speed_mean_m_s": -1.4057665194330719e-05,
  "peak_tilt_rad": 0.14338706063901818,
  "peak_wheel_torque_nm": 1.864382028579712,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6616069658500848,
  "final_integral_m_s": 0.6616069658500848,
  "elapsed_wall_s": 9.503200614009984
}
```
