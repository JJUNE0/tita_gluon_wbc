# tita_flash_sac_193248_068255_model_50000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087",
  "onnx_sha256": "9edc5ad830f2e0f0d88dcb9bd8a21a023d3cdd754ce2e54339650dc66d2bb1c4",
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
  "initial_physics_sha256": "42a3084ae0f47100da96bb8d55432a9e8c980d879e4abee73d11140d4a6dd3dc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.11991339452160962,
  "max_drift_m": 0.11991339452160962,
  "radial_IAE_m_s": 6.794511185909198,
  "signed_longitudinal_delta_m": 0.11991316218671622,
  "tail_speed_mean_m_s": 6.126950304873269e-05,
  "tail_speed_rms_m_s": 6.286750535153099e-05,
  "tail_sensor_speed_mean_m_s": 6.10470719258374e-05,
  "tail_fk_speed_mean_m_s": 6.213102682462782e-05,
  "peak_tilt_rad": 0.050683204384495806,
  "peak_wheel_torque_nm": 0.5550844073295593,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6966889815466079,
  "final_integral_m_s": 0.6966889815466079,
  "elapsed_wall_s": 8.500464865996037
}
```
