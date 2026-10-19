# tita_flash_sac_193248_068255_model_30000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "3f2f1105bf577a63faa630cab51de587908027acec9ac255603fcaf108e74c99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00855067383583809,
  "max_drift_m": 0.017064768487854508,
  "radial_IAE_m_s": 0.5133514711997926,
  "signed_longitudinal_delta_m": -0.00854600692916716,
  "tail_speed_mean_m_s": -7.338617227414818e-06,
  "tail_speed_rms_m_s": 1.114567770782549e-05,
  "tail_sensor_speed_mean_m_s": -7.08270206233701e-06,
  "tail_fk_speed_mean_m_s": -7.392360824298424e-06,
  "peak_tilt_rad": 0.023481849920824915,
  "peak_wheel_torque_nm": 0.3797604739665985,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.11023443200608535,
  "final_integral_m_s": 0.11023443200608535,
  "elapsed_wall_s": 7.972928914008662
}
```
