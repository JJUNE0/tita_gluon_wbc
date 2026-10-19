# tita_flash_sac_115632_883848_model_20000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "800dba170892ea0f36fc1c81fa458e9fa2a8e59fb20de6f730e468cc97d9c4f3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.65294453184231,
  "max_drift_m": 9.65294453184231,
  "radial_IAE_m_s": 288.7849380682761,
  "signed_longitudinal_delta_m": 9.550255813905496,
  "tail_speed_mean_m_s": 0.16259422964957443,
  "tail_speed_rms_m_s": 0.16259753956831172,
  "tail_sensor_speed_mean_m_s": 0.16224888914436306,
  "tail_fk_speed_mean_m_s": 0.16225109001563337,
  "peak_tilt_rad": 0.19498930581815999,
  "peak_wheel_torque_nm": 0.9940102100372314,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.768773219024297
}
```
