# tita_flash_sac_115632_883848_model_95000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "54f8a8ede657dc123cc7dc346693b41539b212002fd58c90895854e2a1e4797b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.038891127346650414,
  "max_drift_m": 0.038891127346650414,
  "radial_IAE_m_s": 1.7535002390163323,
  "signed_longitudinal_delta_m": 0.03888725533433008,
  "tail_speed_mean_m_s": 0.0003186248866445784,
  "tail_speed_rms_m_s": 0.00031901095759460403,
  "tail_sensor_speed_mean_m_s": 0.0003176996714601231,
  "tail_fk_speed_mean_m_s": 0.00031840581641669565,
  "peak_tilt_rad": 0.06265583432725452,
  "peak_wheel_torque_nm": 0.21746982634067535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1980567737864199,
  "final_integral_m_s": 0.1980567737864199,
  "elapsed_wall_s": 13.621935455012135
}
```
