# tita_flash_sac_193248_068255_model_20000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "initial_physics_sha256": "32eb33d395ab1db4a49313db0c4b033371796ef1312e6544bd345e25d00b93ad",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.011272974975773512,
  "max_drift_m": 0.08494814122267141,
  "radial_IAE_m_s": 3.3853248496410773,
  "signed_longitudinal_delta_m": 0.004579102524279378,
  "tail_speed_mean_m_s": -7.883645304425833e-05,
  "tail_speed_rms_m_s": 7.989564357921394e-05,
  "tail_sensor_speed_mean_m_s": -6.703641613383686e-05,
  "tail_fk_speed_mean_m_s": -5.1679558414470085e-05,
  "peak_tilt_rad": 0.1507348293588744,
  "peak_wheel_torque_nm": 1.5590095520019531,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6493489021921699,
  "final_integral_m_s": 0.6493489021921699,
  "elapsed_wall_s": 43.623923154955264
}
```
