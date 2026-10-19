# tita_flash_sac_193248_068255_model_80000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "c4039e1f93449811e54698dfe2a1785252d33f2a587c05b8b70345e0bd4b668e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.239072152457792,
  "max_drift_m": 9.239072152457792,
  "radial_IAE_m_s": 281.3182065780192,
  "signed_longitudinal_delta_m": -9.12132427077937,
  "tail_speed_mean_m_s": -0.15089618673696317,
  "tail_speed_rms_m_s": 0.15173469818243723,
  "tail_sensor_speed_mean_m_s": -0.14972742875251382,
  "tail_fk_speed_mean_m_s": -0.15073332610274962,
  "peak_tilt_rad": 0.08933027961536655,
  "peak_wheel_torque_nm": 4.9257073402404785,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.907022055005655
}
```
