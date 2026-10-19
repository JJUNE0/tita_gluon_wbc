# tita_flash_sac_115632_883848_model_25000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "63c6e183e3f88bd83544dd499f0e7e6f50424987acedd45c004963c2a3147373",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.08179883851419101,
  "max_drift_m": 0.17139102037857235,
  "radial_IAE_m_s": 27.484909052965854,
  "signed_longitudinal_delta_m": 0.07942393857135503,
  "tail_speed_mean_m_s": -0.00022240160307335848,
  "tail_speed_rms_m_s": 0.00022262213326208985,
  "tail_sensor_speed_mean_m_s": -0.00022845873939296378,
  "tail_fk_speed_mean_m_s": -0.00021014188702538086,
  "peak_tilt_rad": 0.1390989166205483,
  "peak_wheel_torque_nm": 2.048210859298706,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.2713134628965952,
  "final_integral_m_s": 1.2713134628965952,
  "elapsed_wall_s": 58.47309719497571
}
```
