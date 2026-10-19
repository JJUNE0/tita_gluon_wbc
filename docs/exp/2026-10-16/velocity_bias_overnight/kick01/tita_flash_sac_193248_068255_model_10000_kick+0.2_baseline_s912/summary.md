# tita_flash_sac_193248_068255_model_10000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "a2b6ee02ca7927eea13675610b35b7d3363db46a783a01a2bc306494aefb47da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.3871527752480664,
  "max_drift_m": 0.3871527752480664,
  "radial_IAE_m_s": 12.838074389357566,
  "signed_longitudinal_delta_m": 0.3830783235320142,
  "tail_speed_mean_m_s": 0.006170954350712882,
  "tail_speed_rms_m_s": 0.0061743806840430125,
  "tail_sensor_speed_mean_m_s": 0.006178679041078362,
  "tail_fk_speed_mean_m_s": 0.006185800377730442,
  "peak_tilt_rad": 0.0452994503444879,
  "peak_wheel_torque_nm": 2.4187159538269043,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.62653460301226
}
```
