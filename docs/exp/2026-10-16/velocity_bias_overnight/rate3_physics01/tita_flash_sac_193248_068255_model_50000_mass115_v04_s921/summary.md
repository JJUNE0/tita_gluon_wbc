# tita_flash_sac_193248_068255_model_50000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "2855f36cbb78a6aa2645823863b680e968433d754d27a8b1dc6e35235ecc0163",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003903560745685597,
  "max_drift_m": 0.021343373221634203,
  "radial_IAE_m_s": 0.7999079545130892,
  "signed_longitudinal_delta_m": 0.003903559894545425,
  "tail_speed_mean_m_s": -0.00042479189939555276,
  "tail_speed_rms_m_s": 0.017513111676746105,
  "tail_sensor_speed_mean_m_s": 0.0026085746760564125,
  "tail_fk_speed_mean_m_s": 2.9340485737733273e-05,
  "peak_tilt_rad": 0.08396342923620081,
  "peak_wheel_torque_nm": 5.938851833343506,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1508408294504209,
  "final_integral_m_s": 0.1508408294504209,
  "elapsed_wall_s": 7.34392051998293
}
```
