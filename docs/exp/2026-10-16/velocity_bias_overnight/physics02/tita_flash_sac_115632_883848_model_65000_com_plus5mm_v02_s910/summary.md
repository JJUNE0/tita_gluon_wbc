# tita_flash_sac_115632_883848_model_65000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_65000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "a28e8551929d9a4412f571a2e91577da75879477c15d61f0774ab6f05354dff3",
  "onnx_sha256": "7cc289e8aee44513f1e29487c7522e96c762174e2444aedaa7aea78b3a66a3ec",
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
  "initial_physics_sha256": "3547ae91e67bd228ae4a304158fce9982ab9dab3b9ec43a516570ab79fa35e2d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008319755437136993,
  "max_drift_m": 0.020396216953689227,
  "radial_IAE_m_s": 0.5248274939527465,
  "signed_longitudinal_delta_m": 0.008318167731872494,
  "tail_speed_mean_m_s": -1.1077150488461295e-05,
  "tail_speed_rms_m_s": 1.1083762852596136e-05,
  "tail_sensor_speed_mean_m_s": -1.0758347187994162e-05,
  "tail_fk_speed_mean_m_s": -1.207120872479671e-05,
  "peak_tilt_rad": 0.06085601253725792,
  "peak_wheel_torque_nm": 0.5451605319976807,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08768175663964792,
  "final_integral_m_s": 0.08770503746607837,
  "elapsed_wall_s": 18.503642033960205
}
```
