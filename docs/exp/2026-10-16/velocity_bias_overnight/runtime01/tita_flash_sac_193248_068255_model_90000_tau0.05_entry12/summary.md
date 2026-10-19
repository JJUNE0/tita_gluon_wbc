# tita_flash_sac_193248_068255_model_90000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "964e1b30ace901dc2a61eef9c00435befffe6331f7fcd7e7774e1880df4088aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06326729919326761,
  "max_drift_m": 0.07269815954731461,
  "radial_IAE_m_s": 3.6596329933458174,
  "signed_longitudinal_delta_m": 0.06326532350797624,
  "tail_speed_mean_m_s": 6.576735710174444e-05,
  "tail_speed_rms_m_s": 6.609026316745515e-05,
  "tail_sensor_speed_mean_m_s": 6.590208688261912e-05,
  "tail_fk_speed_mean_m_s": 6.726695642260977e-05,
  "peak_tilt_rad": 0.10173462868396999,
  "peak_wheel_torque_nm": 1.9393024444580078,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6364253393722733,
  "final_integral_m_s": 0.636315782453286,
  "elapsed_wall_s": 17.94608209002763
}
```
