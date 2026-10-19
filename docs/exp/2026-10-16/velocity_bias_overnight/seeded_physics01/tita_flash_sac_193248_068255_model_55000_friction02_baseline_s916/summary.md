# tita_flash_sac_193248_068255_model_55000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "e24070c2c8dbfaf165112b595c0ca23afcd5b7d10e028ee88e95fbab91d2282c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 19.446110149001164,
  "max_drift_m": 19.446110149001164,
  "radial_IAE_m_s": 586.8807189107915,
  "signed_longitudinal_delta_m": 19.076620115972723,
  "tail_speed_mean_m_s": 0.3242457948024923,
  "tail_speed_rms_m_s": 0.3242457959181552,
  "tail_sensor_speed_mean_m_s": 0.3235432609500222,
  "tail_fk_speed_mean_m_s": 0.3235365343568699,
  "peak_tilt_rad": 0.18032909254317153,
  "peak_wheel_torque_nm": 0.20042765140533447,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.900512322958093
}
```
