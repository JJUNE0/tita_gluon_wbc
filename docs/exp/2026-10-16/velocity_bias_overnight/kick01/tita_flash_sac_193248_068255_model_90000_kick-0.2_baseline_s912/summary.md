# tita_flash_sac_193248_068255_model_90000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "dec31dce230a0bb4e14997abd4767202737e2dae37c75bc32bd4850f31422535",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.761509030115581,
  "max_drift_m": 12.761509030115581,
  "radial_IAE_m_s": 366.90582665537175,
  "signed_longitudinal_delta_m": 12.754024877512862,
  "tail_speed_mean_m_s": 0.22349784225911656,
  "tail_speed_rms_m_s": 0.2234979653616742,
  "tail_sensor_speed_mean_m_s": 0.22301442352991,
  "tail_fk_speed_mean_m_s": 0.22301206664427306,
  "peak_tilt_rad": 0.1119766161050908,
  "peak_wheel_torque_nm": 3.6501951217651367,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.592594826011918
}
```
