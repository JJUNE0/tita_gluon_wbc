# tita_flash_sac_193248_068255_model_90000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "44a419d93f996f559fab465d0be700867e9b791f6aa418c4c58d6af8a946369e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06242902343653013,
  "max_drift_m": 0.07354182079309332,
  "radial_IAE_m_s": 3.594284651197333,
  "signed_longitudinal_delta_m": 0.06242747266368856,
  "tail_speed_mean_m_s": 7.022664354210954e-05,
  "tail_speed_rms_m_s": 7.023793983471435e-05,
  "tail_sensor_speed_mean_m_s": 7.031194037363344e-05,
  "tail_fk_speed_mean_m_s": 7.163485377752464e-05,
  "peak_tilt_rad": 0.1007181504943584,
  "peak_wheel_torque_nm": 1.9385168552398682,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6284159389456886,
  "final_integral_m_s": 0.6282769059266563,
  "elapsed_wall_s": 16.55808096396504
}
```
