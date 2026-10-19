# tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "initial_physics_sha256": "f66e80579add47f1935e6e59ce8ed30ed45e1abccfb1e12fe704cde35c963425",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.027048107862475,
  "max_drift_m": 15.027048107862475,
  "radial_IAE_m_s": 440.28724307839957,
  "signed_longitudinal_delta_m": -14.381725616487534,
  "tail_speed_mean_m_s": -0.25959281513812194,
  "tail_speed_rms_m_s": 0.2596051598910144,
  "tail_sensor_speed_mean_m_s": -0.25918538609851377,
  "tail_fk_speed_mean_m_s": -0.2591965036338046,
  "peak_tilt_rad": 0.03628093927447984,
  "peak_wheel_torque_nm": 0.22329986095428467,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.961218156036921
}
```
