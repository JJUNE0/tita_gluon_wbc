# tita_flash_sac_115632_883848_model_25000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "b1f147547b4b1231ee5a3b0956689c5ac5a185dc0269dc27cc2edca98f01028c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017781381001095272,
  "max_drift_m": 0.02846473465817226,
  "radial_IAE_m_s": 1.0676911915993816,
  "signed_longitudinal_delta_m": 0.017776022516752685,
  "tail_speed_mean_m_s": 5.033105497024605e-07,
  "tail_speed_rms_m_s": 6.294946468527736e-07,
  "tail_sensor_speed_mean_m_s": 5.321779220692937e-07,
  "tail_fk_speed_mean_m_s": 1.1617683330204923e-06,
  "peak_tilt_rad": 0.11898761954201764,
  "peak_wheel_torque_nm": 1.2776029109954834,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18138293924810145,
  "final_integral_m_s": 0.18138209035605968,
  "elapsed_wall_s": 11.568000811035745
}
```
