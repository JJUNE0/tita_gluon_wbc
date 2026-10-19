# tita_flash_sac_193248_068255_model_50000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 948c108cb4740ede74b9c33fdca02f3a0bc4ae70aeb862e20f90c841243b1087

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_50000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "d5e320525d0c9188b3c68bdcca8c56fdc42e600977cc68d77ecac29d2231e9b5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.11973313195728749,
  "max_drift_m": 0.11973313195728749,
  "radial_IAE_m_s": 6.791388699591611,
  "signed_longitudinal_delta_m": 0.11973286162580153,
  "tail_speed_mean_m_s": 5.7092666488731224e-05,
  "tail_speed_rms_m_s": 5.789591376028668e-05,
  "tail_sensor_speed_mean_m_s": 5.6903337667718867e-05,
  "tail_fk_speed_mean_m_s": 5.796285779721983e-05,
  "peak_tilt_rad": 0.05075568458954938,
  "peak_wheel_torque_nm": 0.5586389899253845,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6970904384477409,
  "final_integral_m_s": 0.6970904384477409,
  "elapsed_wall_s": 12.142720925970934
}
```
