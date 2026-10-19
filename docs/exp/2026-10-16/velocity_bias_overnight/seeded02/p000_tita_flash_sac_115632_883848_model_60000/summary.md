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
      "ki": 3.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.0035992338772227986,
  "max_drift_m": 0.008681955235354467,
  "radial_IAE_m_s": 0.24183945113195904,
  "signed_longitudinal_delta_m": 0.0035824953476764143,
  "tail_speed_mean_m_s": -3.29727397063593e-05,
  "tail_speed_rms_m_s": 3.36437483431826e-05,
  "tail_sensor_speed_mean_m_s": -3.2996438952044425e-05,
  "tail_fk_speed_mean_m_s": -3.08562021355945e-05,
  "peak_tilt_rad": 0.06924175608200489,
  "peak_wheel_torque_nm": 0.18832626938819885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04739311072284004,
  "final_integral_m_s": 0.04739311072284004,
  "elapsed_wall_s": 5.153388343984261
}
```
