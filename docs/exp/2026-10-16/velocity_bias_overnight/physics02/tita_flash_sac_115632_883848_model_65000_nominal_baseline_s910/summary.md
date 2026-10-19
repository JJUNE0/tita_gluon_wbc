# tita_flash_sac_115632_883848_model_65000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "a63eaf010b0c141571cf8f6267bae4a8ef07e2c30535073bc45fa22cc0eb46a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.983621835149814,
  "max_drift_m": 1.983621835149814,
  "radial_IAE_m_s": 60.587908091281925,
  "signed_longitudinal_delta_m": 1.976275513252081,
  "tail_speed_mean_m_s": 0.03178613926148656,
  "tail_speed_rms_m_s": 0.03179013846805398,
  "tail_sensor_speed_mean_m_s": 0.03171726496667607,
  "tail_fk_speed_mean_m_s": 0.03171612743217663,
  "peak_tilt_rad": 0.05957089138945082,
  "peak_wheel_torque_nm": 0.25040459632873535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.746173387975432
}
```
