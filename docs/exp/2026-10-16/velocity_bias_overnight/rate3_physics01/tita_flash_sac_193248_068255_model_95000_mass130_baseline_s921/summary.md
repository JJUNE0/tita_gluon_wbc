# tita_flash_sac_193248_068255_model_95000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "9810ad2b386829ed37d61091ee397be60ff857f9b7e8e35d3c05c6c5fe43be31",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 20.602551408343494,
  "max_drift_m": 20.602551408343494,
  "radial_IAE_m_s": 615.1116736490654,
  "signed_longitudinal_delta_m": -20.55045563932553,
  "tail_speed_mean_m_s": -0.3454802801803427,
  "tail_speed_rms_m_s": 0.3454802805417184,
  "tail_sensor_speed_mean_m_s": -0.3447544572527371,
  "tail_fk_speed_mean_m_s": -0.34475388749121844,
  "peak_tilt_rad": 0.062047000330205826,
  "peak_wheel_torque_nm": 0.5424085855484009,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.18129981099628
}
```
