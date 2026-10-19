# tita_flash_sac_115632_883848_model_60000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "5315c098dcd443d4a8a510dca0c01095167d1a6b45c0eaab75c14ce8c3d1712e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.7668298872433917,
  "max_drift_m": 0.7668298872433917,
  "radial_IAE_m_s": 19.654222810258016,
  "signed_longitudinal_delta_m": 0.7659654573132317,
  "tail_speed_mean_m_s": 0.015648399989574922,
  "tail_speed_rms_m_s": 0.015650665478045823,
  "tail_sensor_speed_mean_m_s": 0.015614488161751362,
  "tail_fk_speed_mean_m_s": 0.01561591512489545,
  "peak_tilt_rad": 0.06950946735801722,
  "peak_wheel_torque_nm": 1.5741358995437622,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.380908219027333
}
```
