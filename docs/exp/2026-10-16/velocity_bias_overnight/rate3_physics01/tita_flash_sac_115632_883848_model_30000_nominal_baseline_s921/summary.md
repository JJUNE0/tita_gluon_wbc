# tita_flash_sac_115632_883848_model_30000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "2e2cb74d4f81b1060cda47ce35a95c7c40871fa6c6b0f0570e0ce6a8614f5c8a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.060747045595974,
  "max_drift_m": 14.060747045595974,
  "radial_IAE_m_s": 426.03002036984805,
  "signed_longitudinal_delta_m": 14.043006073851984,
  "tail_speed_mean_m_s": 0.23132621913061344,
  "tail_speed_rms_m_s": 0.23132630511560906,
  "tail_sensor_speed_mean_m_s": 0.23082513846199457,
  "tail_fk_speed_mean_m_s": 0.23082354482267387,
  "peak_tilt_rad": 0.12712715471637726,
  "peak_wheel_torque_nm": 0.1439880132675171,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.793942353047896
}
```
