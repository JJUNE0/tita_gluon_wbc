# tita_flash_sac_115632_883848_model_45000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "6f721d9f26204e40c5eb90545361dc8d9d2be1251ed98d0817c17de83733e34a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 8.2532216770325,
  "max_drift_m": 8.341184732529895,
  "radial_IAE_m_s": 1628.6996782217734,
  "signed_longitudinal_delta_m": 6.709694704856505,
  "tail_speed_mean_m_s": -0.008958429098628477,
  "tail_speed_rms_m_s": 0.0137642908861902,
  "tail_sensor_speed_mean_m_s": -0.009099457344211989,
  "tail_fk_speed_mean_m_s": -0.008903100537438174,
  "peak_tilt_rad": 0.05215275434546163,
  "peak_wheel_torque_nm": 4.342367172241211,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 51.4914373740321
}
```
