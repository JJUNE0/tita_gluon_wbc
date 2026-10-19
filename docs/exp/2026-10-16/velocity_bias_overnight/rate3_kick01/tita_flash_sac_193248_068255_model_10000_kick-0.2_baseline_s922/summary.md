# tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "e44375acf7d7ed33153816eba75bfc2a265b8f97b0b6f14b413e776431f4548a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2568534300850842,
  "max_drift_m": 0.2568534300850842,
  "radial_IAE_m_s": 6.01423455235415,
  "signed_longitudinal_delta_m": 0.250915804082864,
  "tail_speed_mean_m_s": 0.006228772530532767,
  "tail_speed_rms_m_s": 0.006232201053640006,
  "tail_sensor_speed_mean_m_s": 0.006236256864005035,
  "tail_fk_speed_mean_m_s": 0.006243321548169598,
  "peak_tilt_rad": 0.04067644623611244,
  "peak_wheel_torque_nm": 3.862273931503296,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.193443499971181
}
```
