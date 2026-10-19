# tita_flash_sac_115632_883848_model_25000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "2daa7178043eabf13ebad7dfbd4d88e1f1d63fb6d478a85dc129fa99a055da1d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07220431748293464,
  "max_drift_m": 0.10709512241782002,
  "radial_IAE_m_s": 4.255444886954457,
  "signed_longitudinal_delta_m": 0.07219557455746131,
  "tail_speed_mean_m_s": 3.1276307394752885e-05,
  "tail_speed_rms_m_s": 3.2569363707481625e-05,
  "tail_sensor_speed_mean_m_s": 3.1148886785641996e-05,
  "tail_fk_speed_mean_m_s": 3.4464245093597884e-05,
  "peak_tilt_rad": 0.13298341788221313,
  "peak_wheel_torque_nm": 1.3368111848831177,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.745321946035353,
  "final_integral_m_s": 0.7452879624161809,
  "elapsed_wall_s": 12.630911707004998
}
```
