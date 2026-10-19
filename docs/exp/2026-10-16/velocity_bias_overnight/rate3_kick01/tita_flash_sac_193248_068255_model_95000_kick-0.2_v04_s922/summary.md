# tita_flash_sac_193248_068255_model_95000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "0024d98e4d72350969d522c588b63c0928d37af94c0bd045cf2f0ec73c7be9e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012454100610066477,
  "max_drift_m": 0.20625210524966595,
  "radial_IAE_m_s": 1.6372399792673178,
  "signed_longitudinal_delta_m": 0.012341856871893679,
  "tail_speed_mean_m_s": -3.0991900594656245e-06,
  "tail_speed_rms_m_s": 4.9905803711934384e-05,
  "tail_sensor_speed_mean_m_s": -3.307234701296261e-06,
  "tail_fk_speed_mean_m_s": -3.4836702290739537e-06,
  "peak_tilt_rad": 0.12955301772611194,
  "peak_wheel_torque_nm": 1.7536392211914062,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2363249736784369,
  "final_integral_m_s": -0.2363249736784369,
  "elapsed_wall_s": 10.029122538049705
}
```
