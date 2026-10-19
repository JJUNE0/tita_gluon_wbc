# tita_flash_sac_193248_068255_model_75000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "0145a3a08424ae040fce520e56aec0e6fa38c4eabe47ad1908f46e4f2283c0c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011695071210725914,
  "max_drift_m": 0.04099632173647347,
  "radial_IAE_m_s": 0.7925917063316144,
  "signed_longitudinal_delta_m": -0.011693181376948872,
  "tail_speed_mean_m_s": 3.473071327288426e-05,
  "tail_speed_rms_m_s": 3.4735043614053136e-05,
  "tail_sensor_speed_mean_m_s": 3.484219906883432e-05,
  "tail_fk_speed_mean_m_s": 3.430447077424033e-05,
  "peak_tilt_rad": 0.07036152618084257,
  "peak_wheel_torque_nm": 0.42185544967651367,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19106575744707627,
  "final_integral_m_s": -0.19106575744707627,
  "elapsed_wall_s": 9.579820709011983
}
```
