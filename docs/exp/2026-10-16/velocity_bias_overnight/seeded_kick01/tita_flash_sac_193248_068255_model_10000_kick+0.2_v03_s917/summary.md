# tita_flash_sac_193248_068255_model_10000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "ca39f3f15518a1ebff26a9aa1f23c9f8cb4c168ea395c3be70ed09501f7fb3c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035734112232575554,
  "max_drift_m": 0.05166217719068703,
  "radial_IAE_m_s": 2.238123870710915,
  "signed_longitudinal_delta_m": -0.035733182022256206,
  "tail_speed_mean_m_s": 0.00016701694305482483,
  "tail_speed_rms_m_s": 0.00016710804716137494,
  "tail_sensor_speed_mean_m_s": 0.00017969527262359677,
  "tail_fk_speed_mean_m_s": 0.00018624994672860356,
  "peak_tilt_rad": 0.06912247085888534,
  "peak_wheel_torque_nm": 2.4413466453552246,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11509513851542683,
  "final_integral_m_s": 0.11509513851542683,
  "elapsed_wall_s": 12.633181376033463
}
```
