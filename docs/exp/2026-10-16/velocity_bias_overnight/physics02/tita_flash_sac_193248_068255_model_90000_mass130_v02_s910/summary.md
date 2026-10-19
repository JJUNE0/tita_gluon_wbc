# tita_flash_sac_193248_068255_model_90000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "13106ae0f6c66690d47a9edab2961a684a774f0eadea07293f681020e37ff271",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03211170734056321,
  "max_drift_m": 0.033140064130696895,
  "radial_IAE_m_s": 1.2324658705574738,
  "signed_longitudinal_delta_m": -0.03208598217863031,
  "tail_speed_mean_m_s": -0.0003906554832773907,
  "tail_speed_rms_m_s": 0.01699034549200001,
  "tail_sensor_speed_mean_m_s": 0.002930412524040613,
  "tail_fk_speed_mean_m_s": 7.845413298601302e-05,
  "peak_tilt_rad": 0.1611678595161179,
  "peak_wheel_torque_nm": 5.743732452392578,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.08053942109671886,
  "final_integral_m_s": -0.09686691512200124,
  "elapsed_wall_s": 16.45384870300768
}
```
