# tita_flash_sac_115632_883848_model_40000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_40000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "a4b5c15c3add7114e65d55cabbe505c0fffcd993df1b9162587e073cca97a891",
  "onnx_sha256": "4722a7e5dc4a1d465689d98943ba5c9a40a7d45a99344f923f067d1cfa90fcb6",
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
  "initial_physics_sha256": "b7e617799832ffa230e5101505bb37e79d035e2c96e37c51fc3147d7c22e4893",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.077565713313954,
  "max_drift_m": 8.077565713313954,
  "radial_IAE_m_s": 242.94524679882346,
  "signed_longitudinal_delta_m": 8.038278275682753,
  "tail_speed_mean_m_s": 0.13373293664318406,
  "tail_speed_rms_m_s": 0.13373307299414836,
  "tail_sensor_speed_mean_m_s": 0.13344355904058,
  "tail_fk_speed_mean_m_s": 0.1334440822000099,
  "peak_tilt_rad": 0.1196153797809989,
  "peak_wheel_torque_nm": 0.3397941589355469,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.38473101001
}
```
