# tita_flash_sac_193248_068255_model_90000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "13106ae0f6c66690d47a9edab2961a684a774f0eadea07293f681020e37ff271",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.131120277979326,
  "max_drift_m": 4.131120277979326,
  "radial_IAE_m_s": 125.61496699118626,
  "signed_longitudinal_delta_m": -4.130179372085297,
  "tail_speed_mean_m_s": -0.06697413072140902,
  "tail_speed_rms_m_s": 0.06898636011978303,
  "tail_sensor_speed_mean_m_s": -0.06695387680634016,
  "tail_fk_speed_mean_m_s": -0.06673735772869077,
  "peak_tilt_rad": 0.12679109533872102,
  "peak_wheel_torque_nm": 5.33734130859375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.318862783024088
}
```
