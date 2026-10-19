# tita_flash_sac_115632_883848_model_25000_mass115_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass115_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
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
  "initial_physics_sha256": "85ad07916ff3bbea9b742e19b248b5892347d5bfd6af9460aa4611511f1915cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.062418614582308796,
  "max_drift_m": 0.10688185516441638,
  "radial_IAE_m_s": 20.35301903638887,
  "signed_longitudinal_delta_m": 0.06225445816414972,
  "tail_speed_mean_m_s": -3.0074847643658985e-05,
  "tail_speed_rms_m_s": 3.010991578242032e-05,
  "tail_sensor_speed_mean_m_s": -3.072957421021158e-05,
  "tail_fk_speed_mean_m_s": -3.0150150145410025e-05,
  "peak_tilt_rad": 0.1327974847690092,
  "peak_wheel_torque_nm": 1.3183188438415527,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6476382678463443,
  "final_integral_m_s": 0.6477012679741406,
  "elapsed_wall_s": 58.696967753989156
}
```
