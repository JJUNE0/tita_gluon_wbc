# tita_flash_sac_115632_883848_model_25000_friction0.8_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_friction0.8_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "friction": 0.8
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "dc08c599e9441da89084a6970ac0c676d9a7ee9485375bc67ee9c0029cfe1390",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.17982882355164892,
  "max_drift_m": 0.2350846550909163,
  "radial_IAE_m_s": 10.597068244209243,
  "signed_longitudinal_delta_m": 0.1798143873307818,
  "tail_speed_mean_m_s": 8.383864694318753e-05,
  "tail_speed_rms_m_s": 8.475417016716603e-05,
  "tail_sensor_speed_mean_m_s": 9.143713218793006e-05,
  "tail_fk_speed_mean_m_s": 0.00010421221637354622,
  "peak_tilt_rad": 0.12955005653456975,
  "peak_wheel_torque_nm": 1.6360108852386475,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3745858869346907,
  "final_integral_m_s": 1.3744114080691283,
  "elapsed_wall_s": 5.544995917007327
}
```
