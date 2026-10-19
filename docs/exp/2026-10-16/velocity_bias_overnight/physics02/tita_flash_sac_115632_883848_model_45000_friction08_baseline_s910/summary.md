# tita_flash_sac_115632_883848_model_45000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "e571a0e9f378049dc8ebb7b11874ef37b83ff0e8cca5a9be30f8fe1a36693848",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.4939528229230303,
  "max_drift_m": 2.4939528229230303,
  "radial_IAE_m_s": 74.16793202123135,
  "signed_longitudinal_delta_m": 2.451048356754358,
  "tail_speed_mean_m_s": 0.042195280995428915,
  "tail_speed_rms_m_s": 0.04274085540578758,
  "tail_sensor_speed_mean_m_s": 0.04252033788616686,
  "tail_fk_speed_mean_m_s": 0.04207159423754202,
  "peak_tilt_rad": 0.05120964140763107,
  "peak_wheel_torque_nm": 2.609795093536377,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.80037893296685
}
```
