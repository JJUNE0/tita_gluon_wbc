# tita_flash_sac_115632_883848_model_5000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "0bca1a1f42146b7225ce5fd01bc2df7372a3f46d390753ad6bb274bc80d4ce29",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.046171271822304745,
  "max_drift_m": 0.046171271822304745,
  "radial_IAE_m_s": 1.8184774879764425,
  "signed_longitudinal_delta_m": -0.0460476741174678,
  "tail_speed_mean_m_s": -0.0005480871046367969,
  "tail_speed_rms_m_s": 0.019556467858812123,
  "tail_sensor_speed_mean_m_s": -8.180181651994379e-05,
  "tail_fk_speed_mean_m_s": 2.763260514106351e-06,
  "peak_tilt_rad": 0.18482066820974663,
  "peak_wheel_torque_nm": 3.704310894012451,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1806004828548533,
  "final_integral_m_s": -0.1660394749479028,
  "elapsed_wall_s": 20.824560092994943
}
```
