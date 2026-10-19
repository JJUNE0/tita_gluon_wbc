# tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "88bbe47dee9a99809ff0409956d8d23f723c4c55c1f8cf65fa757b7d56cc72f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.493508102338693,
  "max_drift_m": 2.493508102338693,
  "radial_IAE_m_s": 75.04360258641343,
  "signed_longitudinal_delta_m": -2.493358993811998,
  "tail_speed_mean_m_s": -0.04128763353127648,
  "tail_speed_rms_m_s": 0.04128771831435099,
  "tail_sensor_speed_mean_m_s": -0.04122197524388078,
  "tail_fk_speed_mean_m_s": -0.04122119588960683,
  "peak_tilt_rad": 0.04856664222526863,
  "peak_wheel_torque_nm": 0.08390344679355621,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.58116554300068
}
```
