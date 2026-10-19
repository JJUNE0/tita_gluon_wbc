# tita_flash_sac_193248_068255_model_90000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "964e1b30ace901dc2a61eef9c00435befffe6331f7fcd7e7774e1880df4088aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06326945384775494,
  "max_drift_m": 0.07479419352704134,
  "radial_IAE_m_s": 3.6585442812394193,
  "signed_longitudinal_delta_m": 0.06326743433314216,
  "tail_speed_mean_m_s": 6.563092864591865e-05,
  "tail_speed_rms_m_s": 6.598590855425025e-05,
  "tail_sensor_speed_mean_m_s": 6.576284242995227e-05,
  "tail_fk_speed_mean_m_s": 6.713129974583723e-05,
  "peak_tilt_rad": 0.10173462868396999,
  "peak_wheel_torque_nm": 1.9213117361068726,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6364850461778544,
  "final_integral_m_s": 0.6363762648799879,
  "elapsed_wall_s": 15.315503984049428
}
```
