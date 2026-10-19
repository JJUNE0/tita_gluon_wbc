# tita_flash_sac_193248_068255_model_90000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
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
      "slew": 2.0,
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
  "initial_physics_sha256": "380454f869090ce3b5ace6f6d50ea0f7a3dceb83307e5402e8d03e4d39f14bab",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.08970947769679595,
  "max_drift_m": 0.09602348943385043,
  "radial_IAE_m_s": 4.93540336924292,
  "signed_longitudinal_delta_m": 0.08970943134207582,
  "tail_speed_mean_m_s": 0.00016931880810141023,
  "tail_speed_rms_m_s": 0.00017010281374215563,
  "tail_sensor_speed_mean_m_s": 0.00016917411028014425,
  "tail_fk_speed_mean_m_s": 0.0001705853656527006,
  "peak_tilt_rad": 0.10162931056913749,
  "peak_wheel_torque_nm": 3.3046417236328125,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6355309971305775,
  "final_integral_m_s": 0.6355309971305775,
  "elapsed_wall_s": 10.327038467978127
}
```
