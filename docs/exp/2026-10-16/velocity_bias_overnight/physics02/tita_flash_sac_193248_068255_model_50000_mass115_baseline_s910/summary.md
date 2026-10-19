# tita_flash_sac_193248_068255_model_50000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "adebfde77d3422b87e1d133e8d81e7e29b9750682643e1294ed1c2da79438f4b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2650682335562085,
  "max_drift_m": 1.2650682335562085,
  "radial_IAE_m_s": 36.650286661479456,
  "signed_longitudinal_delta_m": 1.2613885636178526,
  "tail_speed_mean_m_s": 0.022256578756029433,
  "tail_speed_rms_m_s": 0.02692030905790043,
  "tail_sensor_speed_mean_m_s": 0.022531395680476095,
  "tail_fk_speed_mean_m_s": 0.02265477861610194,
  "peak_tilt_rad": 0.08753947708866305,
  "peak_wheel_torque_nm": 5.427227973937988,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.660760227998253
}
```
