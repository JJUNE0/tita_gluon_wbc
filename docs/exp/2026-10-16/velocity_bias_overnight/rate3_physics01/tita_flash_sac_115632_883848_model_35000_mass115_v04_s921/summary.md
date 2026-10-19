# tita_flash_sac_115632_883848_model_35000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "5ff7b58c4837bcaf645fe29401a8973f322941cf53723ae3348b26df7a625d08",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009797755217185043,
  "max_drift_m": 0.04181718349582665,
  "radial_IAE_m_s": 0.5367135492863224,
  "signed_longitudinal_delta_m": 0.00979590933397378,
  "tail_speed_mean_m_s": 5.261661712101414e-05,
  "tail_speed_rms_m_s": 5.2670142867505636e-05,
  "tail_sensor_speed_mean_m_s": 5.2676357267262624e-05,
  "tail_fk_speed_mean_m_s": 5.378901967805001e-05,
  "peak_tilt_rad": 0.13542453658478415,
  "peak_wheel_torque_nm": 1.617080807685852,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.35191128410897554,
  "final_integral_m_s": 0.35191128410897554,
  "elapsed_wall_s": 10.258093451964669
}
```
