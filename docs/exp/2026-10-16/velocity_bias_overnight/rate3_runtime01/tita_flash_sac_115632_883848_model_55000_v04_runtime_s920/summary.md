# tita_flash_sac_115632_883848_model_55000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "7d5b7b6fd12327d1c5850bd3874464277846c860ae54c1687923db195ba3c2ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008578109535083702,
  "max_drift_m": 0.04583035848163113,
  "radial_IAE_m_s": 0.49544369776289265,
  "signed_longitudinal_delta_m": -0.00857581895814586,
  "tail_speed_mean_m_s": -4.110519409761716e-05,
  "tail_speed_rms_m_s": 4.1304294242897276e-05,
  "tail_sensor_speed_mean_m_s": -4.043382606989793e-05,
  "tail_fk_speed_mean_m_s": -3.710475018514223e-05,
  "peak_tilt_rad": 0.08956284173154061,
  "peak_wheel_torque_nm": 0.9445213079452515,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24066730260366062,
  "final_integral_m_s": 0.24066730260366062,
  "elapsed_wall_s": 12.237341144995298
}
```
