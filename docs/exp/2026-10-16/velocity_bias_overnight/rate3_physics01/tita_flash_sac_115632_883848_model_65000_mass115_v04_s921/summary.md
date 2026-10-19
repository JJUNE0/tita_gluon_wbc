# tita_flash_sac_115632_883848_model_65000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "de5e8dbb0bd320367347c73fe1f63ff3f2502986f8e0ddb346baa0ac2dc4dd42",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02995435790320519,
  "max_drift_m": 0.06947915843930906,
  "radial_IAE_m_s": 1.8337031894003937,
  "signed_longitudinal_delta_m": 0.029945763249980516,
  "tail_speed_mean_m_s": -5.051392897150454e-06,
  "tail_speed_rms_m_s": 5.1580398613805084e-06,
  "tail_sensor_speed_mean_m_s": -5.152773221091813e-06,
  "tail_fk_speed_mean_m_s": -6.401756154183092e-06,
  "peak_tilt_rad": 0.11575197526227732,
  "peak_wheel_torque_nm": 1.0215120315551758,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21403173175210555,
  "final_integral_m_s": -0.21403173175210555,
  "elapsed_wall_s": 6.620511928980704
}
```
