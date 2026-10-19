# tita_flash_sac_193248_068255_model_10000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "c4fda80c28318d62943cc3e658941036df7617eaa635bee4dff3cd728c8c19da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06341774636678697,
  "max_drift_m": 0.06446233034825485,
  "radial_IAE_m_s": 3.6996339556844995,
  "signed_longitudinal_delta_m": -0.06341738437460885,
  "tail_speed_mean_m_s": 2.6766744249148978e-05,
  "tail_speed_rms_m_s": 2.677322567188252e-05,
  "tail_sensor_speed_mean_m_s": 2.8467913873923832e-05,
  "tail_fk_speed_mean_m_s": 3.1327733670860345e-05,
  "peak_tilt_rad": 0.060129262398318284,
  "peak_wheel_torque_nm": 0.9322301149368286,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35663138973503283,
  "final_integral_m_s": -0.35663138973503283,
  "elapsed_wall_s": 9.537706667964812
}
```
