# tita_flash_sac_193248_068255_model_25000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "708e091eae3c1b579470048e57bf0389523d4317e36bcd212edf15853bed068e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.375191651095118,
  "max_drift_m": 10.375191651095118,
  "radial_IAE_m_s": 312.354276440062,
  "signed_longitudinal_delta_m": 10.36992265955517,
  "tail_speed_mean_m_s": 0.1716438111943867,
  "tail_speed_rms_m_s": 0.17164390015168238,
  "tail_sensor_speed_mean_m_s": 0.17127224388305357,
  "tail_fk_speed_mean_m_s": 0.17127195319130487,
  "peak_tilt_rad": 0.1060057700939836,
  "peak_wheel_torque_nm": 0.1024618148803711,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.312163352966309
}
```
