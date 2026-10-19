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
  "initial_physics_sha256": "ca39f3f15518a1ebff26a9aa1f23c9f8cb4c168ea395c3be70ed09501f7fb3c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02141606486252232,
  "max_drift_m": 0.05510378847969111,
  "radial_IAE_m_s": 1.1717747902339604,
  "signed_longitudinal_delta_m": 0.021360660885170947,
  "tail_speed_mean_m_s": 0.00017049044174722227,
  "tail_speed_rms_m_s": 0.00017057868508996567,
  "tail_sensor_speed_mean_m_s": 0.00018385002863716956,
  "tail_fk_speed_mean_m_s": 0.00019054853647606859,
  "peak_tilt_rad": 0.04489387741768702,
  "peak_wheel_torque_nm": 2.4190025329589844,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11193394796906017,
  "final_integral_m_s": 0.11193394796906017,
  "elapsed_wall_s": 9.63842727796873
}
```
