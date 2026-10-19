# tita_flash_sac_193248_068255_model_90000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "fb813b4977f9988404b3f4c1258caf7f08a427944f860d05b4d1228eb78cde60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09604576659426338,
  "max_drift_m": 0.10278535007410744,
  "radial_IAE_m_s": 5.263511726234239,
  "signed_longitudinal_delta_m": 0.09604559740171285,
  "tail_speed_mean_m_s": 0.0002504013868343607,
  "tail_speed_rms_m_s": 0.0002517178261523684,
  "tail_sensor_speed_mean_m_s": 0.0002499801124283929,
  "tail_fk_speed_mean_m_s": 0.00025136009625161926,
  "peak_tilt_rad": 0.09576618957027838,
  "peak_wheel_torque_nm": 1.7310255765914917,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5440269031143862,
  "final_integral_m_s": 0.5440269031143862,
  "elapsed_wall_s": 7.232860516000073
}
```
