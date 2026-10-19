# tita_flash_sac_193248_068255_model_90000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "ffa0acfcd553e4885a3289e3ce14ad7e2b6fb0d204b018140b12f9840d94661c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09136454908102191,
  "max_drift_m": 0.10857648493747965,
  "radial_IAE_m_s": 5.1450223218897015,
  "signed_longitudinal_delta_m": 0.09136423954408858,
  "tail_speed_mean_m_s": 0.00016558820401105101,
  "tail_speed_rms_m_s": 0.0001666075995645144,
  "tail_sensor_speed_mean_m_s": 0.0001655268583654652,
  "tail_fk_speed_mean_m_s": 0.00016687331699460063,
  "peak_tilt_rad": 0.1017346416185243,
  "peak_wheel_torque_nm": 1.6773808002471924,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6366886289866432,
  "final_integral_m_s": 0.6366886289866432,
  "elapsed_wall_s": 11.967259702971205
}
```
