# tita_flash_sac_193248_068255_model_40000_seeded_v03_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_seeded_v03_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "guarded": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "fdbd5c08e02c6001edafb96c7cfb471458a82119dbbd2bf35364658dd8d63dce",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014183530413146806,
  "max_drift_m": 0.04344385234336117,
  "radial_IAE_m_s": 1.020869422490368,
  "signed_longitudinal_delta_m": -0.014183530406308351,
  "tail_speed_mean_m_s": 7.690426441169021e-05,
  "tail_speed_rms_m_s": 7.69375162925332e-05,
  "tail_sensor_speed_mean_m_s": 7.70915010706864e-05,
  "tail_fk_speed_mean_m_s": 7.647478933020798e-05,
  "peak_tilt_rad": 0.10886326091797272,
  "peak_wheel_torque_nm": 0.8792065382003784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2603414430824187,
  "final_integral_m_s": 0.2603414430824187,
  "elapsed_wall_s": 4.702745388960466
}
```
