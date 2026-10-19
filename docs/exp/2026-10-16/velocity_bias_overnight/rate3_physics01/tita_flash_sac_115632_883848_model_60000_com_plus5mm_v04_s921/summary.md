# tita_flash_sac_115632_883848_model_60000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "e6c2bd59e50612f2bdd6c77157e160a62a0ba08c7594c1e0e11aa3d1ef6a88bb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005957796295568677,
  "max_drift_m": 0.01592320325957115,
  "radial_IAE_m_s": 0.059117325799099604,
  "signed_longitudinal_delta_m": -0.0005829727743839443,
  "tail_speed_mean_m_s": -3.576148712508234e-05,
  "tail_speed_rms_m_s": 3.581271166665319e-05,
  "tail_sensor_speed_mean_m_s": -3.5655410624771554e-05,
  "tail_fk_speed_mean_m_s": -3.3798633485829397e-05,
  "peak_tilt_rad": 0.07314758314846714,
  "peak_wheel_torque_nm": 0.295327752828598,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09078043110318827,
  "final_integral_m_s": 0.09078043110318827,
  "elapsed_wall_s": 7.0574145700084046
}
```
