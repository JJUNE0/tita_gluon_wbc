# tita_flash_sac_193248_068255_model_55000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "8c9019b81d4f85f3c581bf67be0e7e3cabc1c311cca53889cc21be2e2a93d4c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.9139330063392404,
  "max_drift_m": 3.9139330063392404,
  "radial_IAE_m_s": 116.07888368203197,
  "signed_longitudinal_delta_m": 3.9122848868017144,
  "tail_speed_mean_m_s": 0.0664157580890419,
  "tail_speed_rms_m_s": 0.06641589117899947,
  "tail_sensor_speed_mean_m_s": 0.06627321772256024,
  "tail_fk_speed_mean_m_s": 0.06627264492629185,
  "peak_tilt_rad": 0.18295837178694985,
  "peak_wheel_torque_nm": 0.36524540185928345,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.943419262999669
}
```
