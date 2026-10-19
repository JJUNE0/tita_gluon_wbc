# tita_flash_sac_193248_068255_model_50000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
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
  "initial_physics_sha256": "604f73a9b7af4ba012f944ce38a832332ded44f60bc228893c63e2be75800597",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.11852685496048383,
  "max_drift_m": 0.11852685496048383,
  "radial_IAE_m_s": 6.530470612097041,
  "signed_longitudinal_delta_m": 0.11852619484957617,
  "tail_speed_mean_m_s": 6.23713811814946e-05,
  "tail_speed_rms_m_s": 6.41210018459426e-05,
  "tail_sensor_speed_mean_m_s": 6.213939278306265e-05,
  "tail_fk_speed_mean_m_s": 6.323050767463373e-05,
  "peak_tilt_rad": 0.050357051607373915,
  "peak_wheel_torque_nm": 2.0673112869262695,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6965825292417236,
  "final_integral_m_s": 0.6965825292417236,
  "elapsed_wall_s": 9.326340958999936
}
```
