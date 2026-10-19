# tita_flash_sac_115632_883848_model_80000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_80000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_80000",
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
  "checkpoint_sha256": "80677a4fd403aad22ca310d644998b9b9a686da481d6d95eaf8cc02aa67afadc",
  "onnx_sha256": "c7a83d6c9814cc6aa8357e4b0215d65d880dd6b756de2de920967396e901c93b",
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
  "initial_physics_sha256": "fc863fb925dbddd0c64c2c68b9b24988dd8687a1802dc908f6d5eb7081209f31",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.047304245487493075,
  "max_drift_m": 0.05689022738568583,
  "radial_IAE_m_s": 2.647630487250618,
  "signed_longitudinal_delta_m": 0.04729257598690317,
  "tail_speed_mean_m_s": 9.861741143621928e-05,
  "tail_speed_rms_m_s": 0.00010016820547448092,
  "tail_sensor_speed_mean_m_s": 9.851436827997742e-05,
  "tail_fk_speed_mean_m_s": 9.926126658601098e-05,
  "peak_tilt_rad": 0.08228383958461283,
  "peak_wheel_torque_nm": 0.44131696224212646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21398562882227543,
  "final_integral_m_s": 0.21398562882227543,
  "elapsed_wall_s": 8.244504834001418
}
```
