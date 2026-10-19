# tita_flash_sac_193248_068255_model_75000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "f3b2d75f8e92ecc39901cb0c30550497c4c01bc9682370d42a7df46bfd5492d9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004821582343289469,
  "max_drift_m": 0.05738105270280578,
  "radial_IAE_m_s": 0.4701818929866447,
  "signed_longitudinal_delta_m": -0.004792547859777115,
  "tail_speed_mean_m_s": 3.83211446902232e-05,
  "tail_speed_rms_m_s": 3.832664846400336e-05,
  "tail_sensor_speed_mean_m_s": 3.8529114059007597e-05,
  "tail_fk_speed_mean_m_s": 3.802210002986873e-05,
  "peak_tilt_rad": 0.08775408125307238,
  "peak_wheel_torque_nm": 0.4379885792732239,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.28884275206358656,
  "final_integral_m_s": -0.28884275206358656,
  "elapsed_wall_s": 6.118361861968879
}
```
