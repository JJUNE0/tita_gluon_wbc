# tita_flash_sac_193248_068255_model_75000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
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
  "initial_physics_sha256": "43c12c6c18dad17414411897690f6f386a5d8893dc7d908f863b09c3cd3afa9c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0034600801567634233,
  "max_drift_m": 0.06842453807767508,
  "radial_IAE_m_s": 0.39571579780945293,
  "signed_longitudinal_delta_m": 0.0033843530538774087,
  "tail_speed_mean_m_s": 1.8604179293665316e-05,
  "tail_speed_rms_m_s": 1.865371668326616e-05,
  "tail_sensor_speed_mean_m_s": 1.8700493007432523e-05,
  "tail_fk_speed_mean_m_s": 1.840265880539445e-05,
  "peak_tilt_rad": 0.09794829071671485,
  "peak_wheel_torque_nm": 0.7712003588676453,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3537549572627703,
  "final_integral_m_s": -0.3537549572627703,
  "elapsed_wall_s": 7.419313792022876
}
```
