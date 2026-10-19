# tita_flash_sac_193248_068255_model_55000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "750dc4a5395e90e609ead780fa688addcc7105b871055df778fba35d07f9ec04",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.006101198463341,
  "max_drift_m": 9.006101198463341,
  "radial_IAE_m_s": 259.28695713071016,
  "signed_longitudinal_delta_m": 8.974804999137257,
  "tail_speed_mean_m_s": 0.15895595759823644,
  "tail_speed_rms_m_s": 0.15895617106549703,
  "tail_sensor_speed_mean_m_s": 0.1586134942483029,
  "tail_fk_speed_mean_m_s": 0.1586108538878652,
  "peak_tilt_rad": 0.18237094581974267,
  "peak_wheel_torque_nm": 0.21661469340324402,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.279373191995546
}
```
