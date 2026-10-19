# tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "initial_physics_sha256": "ca9a6f3157b1f7704d05c6bfc356575fee9c6bee73a05e03c03fa9668271cec9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.4867229541510913,
  "max_drift_m": 3.4867229541510913,
  "radial_IAE_m_s": 106.4927844756436,
  "signed_longitudinal_delta_m": -3.48662033433225,
  "tail_speed_mean_m_s": -0.056901207696932354,
  "tail_speed_rms_m_s": 0.056901277854851946,
  "tail_sensor_speed_mean_m_s": -0.05681204091646387,
  "tail_fk_speed_mean_m_s": -0.05681195263866379,
  "peak_tilt_rad": 0.08955111564504148,
  "peak_wheel_torque_nm": 3.7924094200134277,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.878826352010947
}
```
