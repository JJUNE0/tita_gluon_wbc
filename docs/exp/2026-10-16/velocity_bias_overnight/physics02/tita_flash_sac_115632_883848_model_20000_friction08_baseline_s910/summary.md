# tita_flash_sac_115632_883848_model_20000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "ab04ab81bc0501c9010f0e29b4a07277dbfc9474ba7bb0e9499d8314d61b9867",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.392614377578827,
  "max_drift_m": 14.392614377578827,
  "radial_IAE_m_s": 433.8789790428269,
  "signed_longitudinal_delta_m": 13.940180995638057,
  "tail_speed_mean_m_s": 0.2454540266619691,
  "tail_speed_rms_m_s": 0.24545402670005748,
  "tail_sensor_speed_mean_m_s": 0.24492572853317798,
  "tail_fk_speed_mean_m_s": 0.2448953333979452,
  "peak_tilt_rad": 0.17106122527305256,
  "peak_wheel_torque_nm": 0.36298835277557373,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.402821464987937
}
```
