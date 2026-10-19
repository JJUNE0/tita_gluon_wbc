# tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "0024d98e4d72350969d522c588b63c0928d37af94c0bd045cf2f0ec73c7be9e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.885412460008325,
  "max_drift_m": 8.885412460008325,
  "radial_IAE_m_s": 262.1054618807502,
  "signed_longitudinal_delta_m": -8.691131530677543,
  "tail_speed_mean_m_s": -0.16732579336490683,
  "tail_speed_rms_m_s": 0.16808595438437807,
  "tail_sensor_speed_mean_m_s": -0.167111981288809,
  "tail_fk_speed_mean_m_s": -0.1671310802577637,
  "peak_tilt_rad": 0.044872312707929796,
  "peak_wheel_torque_nm": 1.5768706798553467,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.03869387297891
}
```
