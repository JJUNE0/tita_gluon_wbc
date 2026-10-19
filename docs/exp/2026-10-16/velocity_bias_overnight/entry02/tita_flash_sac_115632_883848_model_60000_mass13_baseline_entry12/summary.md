# tita_flash_sac_115632_883848_model_60000_mass13_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass13_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "5778aa7084ae1a9bdba6b9dda016e1318e27c07ad5f84a80c847cf7b0979bf35",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.424898849223275,
  "max_drift_m": 9.424898849223275,
  "radial_IAE_m_s": 284.88067452084624,
  "signed_longitudinal_delta_m": -9.372354849743228,
  "tail_speed_mean_m_s": -0.1547138726265622,
  "tail_speed_rms_m_s": 0.15472063703257663,
  "tail_sensor_speed_mean_m_s": -0.15438158955291892,
  "tail_fk_speed_mean_m_s": -0.154379184314755,
  "peak_tilt_rad": 0.06652038889689171,
  "peak_wheel_torque_nm": 0.25966596603393555,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.8329079350223765
}
```
