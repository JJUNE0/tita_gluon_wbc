# tita_flash_sac_115632_883848_model_60000_kick+0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "2d9601b51db8284cda41b0827672db1d38f49da51eda58c30c588fe43739f9c3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0709775912788135,
  "max_drift_m": 1.0709775912788135,
  "radial_IAE_m_s": 36.16268583020202,
  "signed_longitudinal_delta_m": 1.0702399518744146,
  "tail_speed_mean_m_s": 0.015842719363674335,
  "tail_speed_rms_m_s": 0.015844611650314682,
  "tail_sensor_speed_mean_m_s": 0.01580842692176946,
  "tail_fk_speed_mean_m_s": 0.01580986276881782,
  "peak_tilt_rad": 0.09691464071218814,
  "peak_wheel_torque_nm": 1.7559731006622314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.10408743500011
}
```
