# tita_flash_sac_193248_068255_model_70000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "e9b4e87cf105d8611032b3b5d1b15f42a36f1d721dc21b3ca252ac882fbf066e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.464986345527948,
  "max_drift_m": 5.464986345527948,
  "radial_IAE_m_s": 154.75602327668582,
  "signed_longitudinal_delta_m": 5.464587869670198,
  "tail_speed_mean_m_s": 0.09977771127576701,
  "tail_speed_rms_m_s": 0.09977828936380162,
  "tail_sensor_speed_mean_m_s": 0.0995627096039866,
  "tail_fk_speed_mean_m_s": 0.09956110497196881,
  "peak_tilt_rad": 0.09054336673897567,
  "peak_wheel_torque_nm": 0.08295436203479767,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.98692202201346
}
```
