# tita_flash_sac_115632_883848_model_95000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "b5ff1c49c2cec8e9eb0b6a08e266bc08c03eb7ce7862755e68273a4c01e436de",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.029777442835030827,
  "max_drift_m": 0.12324790742423539,
  "radial_IAE_m_s": 1.5760602781273891,
  "signed_longitudinal_delta_m": 0.02977744260028947,
  "tail_speed_mean_m_s": 0.00024947287761711216,
  "tail_speed_rms_m_s": 0.0002518253190651077,
  "tail_sensor_speed_mean_m_s": 0.00024885678481751815,
  "tail_fk_speed_mean_m_s": 0.0002494562857303893,
  "peak_tilt_rad": 0.0822663324300632,
  "peak_wheel_torque_nm": 1.8397890329360962,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08396877684806599,
  "final_integral_m_s": 0.08396877684806599,
  "elapsed_wall_s": 6.187684690987226
}
```
