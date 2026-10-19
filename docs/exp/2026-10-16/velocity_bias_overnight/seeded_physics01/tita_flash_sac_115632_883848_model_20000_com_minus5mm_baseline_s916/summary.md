# tita_flash_sac_115632_883848_model_20000_com_minus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_com_minus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "a277e34a7a6d109af96a18b9cc09d2fe3ec2f7c102881ce3b429fb7f09d07d6a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.9742004306546,
  "max_drift_m": 12.9742004306546,
  "radial_IAE_m_s": 388.9607840580794,
  "signed_longitudinal_delta_m": 12.730502873707644,
  "tail_speed_mean_m_s": 0.220180112767425,
  "tail_speed_rms_m_s": 0.22018011310386254,
  "tail_sensor_speed_mean_m_s": 0.21970559452006178,
  "tail_fk_speed_mean_m_s": 0.21968246499351599,
  "peak_tilt_rad": 0.16518099292167343,
  "peak_wheel_torque_nm": 0.3621951937675476,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.223657901980914
}
```
