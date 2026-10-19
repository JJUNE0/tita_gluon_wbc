# tita_flash_sac_193248_068255_model_90000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "08466cae69855888310024418d357952dc27a792d467accab7b42c1314c57c57",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0946808242430651,
  "max_drift_m": 0.10113631655473955,
  "radial_IAE_m_s": 5.621362730158715,
  "signed_longitudinal_delta_m": 0.09467552733269403,
  "tail_speed_mean_m_s": 2.4187832262026024e-05,
  "tail_speed_rms_m_s": 9.809974069945587e-05,
  "tail_sensor_speed_mean_m_s": -5.8481408116456345e-05,
  "tail_fk_speed_mean_m_s": 4.88133169803559e-06,
  "peak_tilt_rad": 0.10293563164290531,
  "peak_wheel_torque_nm": 4.519628524780273,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.7061408255673766,
  "final_integral_m_s": 0.7061408255673766,
  "elapsed_wall_s": 7.358903646992985
}
```
