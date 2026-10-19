# tita_flash_sac_193248_068255_model_90000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "04d417eae262660f91c485880fae49f719133cfcc9fdc3001557dd50151da814",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06252447321864817,
  "max_drift_m": 0.11149165666211534,
  "radial_IAE_m_s": 3.643695513596697,
  "signed_longitudinal_delta_m": 0.06251719770345651,
  "tail_speed_mean_m_s": 5.230150357658588e-05,
  "tail_speed_rms_m_s": 5.2379228680898586e-05,
  "tail_sensor_speed_mean_m_s": 5.2522429504239984e-05,
  "tail_fk_speed_mean_m_s": 5.38910194432877e-05,
  "peak_tilt_rad": 0.109145610095849,
  "peak_wheel_torque_nm": 1.266945242881775,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6548979302550562,
  "final_integral_m_s": 0.6547953003001571,
  "elapsed_wall_s": 4.410039412032347
}
```
