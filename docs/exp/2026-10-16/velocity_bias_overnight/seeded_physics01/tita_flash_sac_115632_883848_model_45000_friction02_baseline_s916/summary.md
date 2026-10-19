# tita_flash_sac_115632_883848_model_45000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "0bf34a909efc1c12a5b9e9c71da62345c21cdac69c26025debfbab296441e834",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1649307753841989,
  "max_drift_m": 0.21199553795637577,
  "radial_IAE_m_s": 9.253540597149545,
  "signed_longitudinal_delta_m": 0.1390044873324731,
  "tail_speed_mean_m_s": 0.005515056012194431,
  "tail_speed_rms_m_s": 0.010732263641044978,
  "tail_sensor_speed_mean_m_s": 0.007093540977337994,
  "tail_fk_speed_mean_m_s": 0.005771373953116512,
  "peak_tilt_rad": 0.0417783978610462,
  "peak_wheel_torque_nm": 3.1701712608337402,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.206653415982146
}
```
