# tita_flash_sac_193248_068255_model_65000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "418ef7f02d176e43b994326f12b9563b6da412b481de3d79fa14fb0ec333854a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.646406577831499,
  "max_drift_m": 2.646406577831499,
  "radial_IAE_m_s": 80.05477493881986,
  "signed_longitudinal_delta_m": -2.6434499162535654,
  "tail_speed_mean_m_s": -0.043294712406747336,
  "tail_speed_rms_m_s": 0.04329532276778837,
  "tail_sensor_speed_mean_m_s": -0.043209448958522884,
  "tail_fk_speed_mean_m_s": -0.04320469032484556,
  "peak_tilt_rad": 0.029539255242556184,
  "peak_wheel_torque_nm": 0.04986970126628876,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.65990700799739
}
```
