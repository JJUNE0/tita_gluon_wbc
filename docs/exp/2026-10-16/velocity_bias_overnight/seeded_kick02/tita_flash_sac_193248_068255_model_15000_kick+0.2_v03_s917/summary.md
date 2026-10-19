# tita_flash_sac_193248_068255_model_15000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "1abdb3b98979f5b9406cf7434a7c594278d82cb0ad28690525ca45b018fd0071",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0004278734203267851,
  "max_drift_m": 0.04206892674571232,
  "radial_IAE_m_s": 0.09957938462644185,
  "signed_longitudinal_delta_m": 0.000403384656967787,
  "tail_speed_mean_m_s": -1.1188908774811014e-05,
  "tail_speed_rms_m_s": 1.1194237393283162e-05,
  "tail_sensor_speed_mean_m_s": -1.1241064157707165e-05,
  "tail_fk_speed_mean_m_s": -8.92857309705497e-06,
  "peak_tilt_rad": 0.08136979448303117,
  "peak_wheel_torque_nm": 2.50846004486084,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18242557322130362,
  "final_integral_m_s": -0.18242557322130362,
  "elapsed_wall_s": 8.971936666988768
}
```
