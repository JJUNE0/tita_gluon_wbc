# tita_flash_sac_115632_883848_model_20000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "96743b0a77931af58e0c503af86f7f76503db2c0484bbb583e85eb0b7cb238b8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.124222560441188,
  "max_drift_m": 14.124222560441188,
  "radial_IAE_m_s": 435.40444902341534,
  "signed_longitudinal_delta_m": 11.313488582122483,
  "tail_speed_mean_m_s": 0.2509290776423094,
  "tail_speed_rms_m_s": 0.25092907764880834,
  "tail_sensor_speed_mean_m_s": 0.2507236604059594,
  "tail_fk_speed_mean_m_s": 0.2507753563849699,
  "peak_tilt_rad": 0.177412301995566,
  "peak_wheel_torque_nm": 0.23092317581176758,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.295689069025684
}
```
