# tita_flash_sac_115632_883848_model_95000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "f399c2c095634ca40da9f58723c9fe3beb1df467323b3f05e9a001be13494557",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08672694065463717,
  "max_drift_m": 0.09584035560908645,
  "radial_IAE_m_s": 5.363795006011144,
  "signed_longitudinal_delta_m": 0.08634571968757328,
  "tail_speed_mean_m_s": 8.900885175008093e-06,
  "tail_speed_rms_m_s": 8.940295317513678e-06,
  "tail_sensor_speed_mean_m_s": 4.7549294948767295e-06,
  "tail_fk_speed_mean_m_s": -1.364602760894865e-07,
  "peak_tilt_rad": 0.06422107651288034,
  "peak_wheel_torque_nm": 0.3048776388168335,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5124317358304675,
  "final_integral_m_s": 0.5124317358304675,
  "elapsed_wall_s": 12.040004673006479
}
```
