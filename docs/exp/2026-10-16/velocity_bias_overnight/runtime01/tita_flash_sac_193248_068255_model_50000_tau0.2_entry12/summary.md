# tita_flash_sac_193248_068255_model_50000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "1315e3204cfff9981202a4e9ceff7e951e07ac26a8155bfa3bf7762d31643676",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06900414080860187,
  "max_drift_m": 0.06900414080860187,
  "radial_IAE_m_s": 4.035484111978093,
  "signed_longitudinal_delta_m": 0.06900257184219544,
  "tail_speed_mean_m_s": 2.089311296017476e-05,
  "tail_speed_rms_m_s": 2.0979452246496678e-05,
  "tail_sensor_speed_mean_m_s": 2.076914273148387e-05,
  "tail_fk_speed_mean_m_s": 2.1839313308135534e-05,
  "peak_tilt_rad": 0.05076176061057436,
  "peak_wheel_torque_nm": 0.47100260853767395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6974069693508959,
  "final_integral_m_s": 0.6973663867201421,
  "elapsed_wall_s": 9.198935087944847
}
```
