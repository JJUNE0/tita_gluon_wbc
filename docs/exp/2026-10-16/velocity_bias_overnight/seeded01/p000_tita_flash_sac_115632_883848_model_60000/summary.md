# p000_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p000_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 0.0,
      "ki": 0.5,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 2.0
    }
  },
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "1252bce4e0207a4aac3c95595d0643b19a94014daa95bb3e2172e4884e2862ed",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04755047420433903,
  "max_drift_m": 0.05069722442098517,
  "radial_IAE_m_s": 2.680904567876609,
  "signed_longitudinal_delta_m": 0.04754571546227947,
  "tail_speed_mean_m_s": -0.00015597259419714688,
  "tail_speed_rms_m_s": 0.00016008722580357517,
  "tail_sensor_speed_mean_m_s": -0.00015577717404776612,
  "tail_fk_speed_mean_m_s": -0.00015357196440371422,
  "peak_tilt_rad": 0.06924175608200489,
  "peak_wheel_torque_nm": 0.15959066152572632,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04771153152970569,
  "final_integral_m_s": 0.04771153152970569,
  "elapsed_wall_s": 5.176372310961597
}
```
