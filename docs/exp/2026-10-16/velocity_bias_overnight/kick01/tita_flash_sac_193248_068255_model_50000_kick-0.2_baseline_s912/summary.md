# tita_flash_sac_193248_068255_model_50000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "190a0bca2e3df0b7a5b5bdc3192ed5b1ab967d9df9039fe023fa35553913d5f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.99431101197988,
  "max_drift_m": 6.99431101197988,
  "radial_IAE_m_s": 197.88986456824776,
  "signed_longitudinal_delta_m": 6.993523953583575,
  "tail_speed_mean_m_s": 0.12626074884070573,
  "tail_speed_rms_m_s": 0.12626534933615674,
  "tail_sensor_speed_mean_m_s": 0.12598790153584763,
  "tail_fk_speed_mean_m_s": 0.12598620866617374,
  "peak_tilt_rad": 0.058429043934922875,
  "peak_wheel_torque_nm": 2.3661201000213623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.88071758399019
}
```
