# tita_flash_sac_193248_068255_model_50000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
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
  "initial_physics_sha256": "2dedf09835742bfcb319e8cd63fb57f321c3fe1ac4fcf6a2f96ef23d4866ee04",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06846871098911342,
  "max_drift_m": 0.06846871098911342,
  "radial_IAE_m_s": 4.028708429675271,
  "signed_longitudinal_delta_m": 0.06846739362635607,
  "tail_speed_mean_m_s": 1.2529393969510735e-05,
  "tail_speed_rms_m_s": 1.3646993240920142e-05,
  "tail_sensor_speed_mean_m_s": 1.2601043642591963e-05,
  "tail_fk_speed_mean_m_s": 1.3475962204434003e-05,
  "peak_tilt_rad": 0.05592421940770498,
  "peak_wheel_torque_nm": 0.9610269665718079,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6992832583627041,
  "final_integral_m_s": 0.6992663723624849,
  "elapsed_wall_s": 4.42420505604241
}
```
