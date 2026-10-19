# tita_flash_sac_193248_068255_model_90000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "3c5676fcc033a2469bf83e574c088c280d3cd4a23eb31715a3b502304270191b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08987003768123618,
  "max_drift_m": 0.09612695041936022,
  "radial_IAE_m_s": 4.949582323616124,
  "signed_longitudinal_delta_m": 0.0898699627652295,
  "tail_speed_mean_m_s": 0.00016608041850956913,
  "tail_speed_rms_m_s": 0.00016708469131197326,
  "tail_sensor_speed_mean_m_s": 0.0001660039090513249,
  "tail_fk_speed_mean_m_s": 0.00016736202843207516,
  "peak_tilt_rad": 0.10173466757515581,
  "peak_wheel_torque_nm": 3.30668306350708,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6364858414254614,
  "final_integral_m_s": 0.6364858414254614,
  "elapsed_wall_s": 12.2389162320178
}
```
