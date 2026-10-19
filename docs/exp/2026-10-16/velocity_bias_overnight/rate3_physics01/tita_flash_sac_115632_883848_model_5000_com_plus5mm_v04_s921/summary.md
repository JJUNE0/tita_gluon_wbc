# tita_flash_sac_115632_883848_model_5000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "efb3ad5c12ac3f9ce5c6c9c2e9a9416ad93953586dc1bd1bc878e96cdbb4806c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025487085003783203,
  "max_drift_m": 0.13235289310188858,
  "radial_IAE_m_s": 1.9301029368350837,
  "signed_longitudinal_delta_m": -0.025461159295608094,
  "tail_speed_mean_m_s": 4.720514898689746e-05,
  "tail_speed_rms_m_s": 5.04505528170173e-05,
  "tail_sensor_speed_mean_m_s": 5.715557475604569e-05,
  "tail_fk_speed_mean_m_s": 6.141024882716175e-05,
  "peak_tilt_rad": 0.19524507762684173,
  "peak_wheel_torque_nm": 2.97538161277771,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.39189710554468155,
  "final_integral_m_s": -0.39189710554468155,
  "elapsed_wall_s": 12.538300994958263
}
```
