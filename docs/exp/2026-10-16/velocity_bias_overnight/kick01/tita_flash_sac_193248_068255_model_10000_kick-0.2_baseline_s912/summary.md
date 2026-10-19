# tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "11f5b361ef849baf096ea386ef715f4a57a5efc9d0dfbf39105668a7243926cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.25685414768450066,
  "max_drift_m": 0.25685414768450066,
  "radial_IAE_m_s": 6.014254537350357,
  "signed_longitudinal_delta_m": 0.2509165221697305,
  "tail_speed_mean_m_s": 0.006228781434522377,
  "tail_speed_rms_m_s": 0.006232209891089904,
  "tail_sensor_speed_mean_m_s": 0.006236264632829286,
  "tail_fk_speed_mean_m_s": 0.006243330657066999,
  "peak_tilt_rad": 0.040676526375189814,
  "peak_wheel_torque_nm": 3.8622629642486572,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.598764255992137
}
```
