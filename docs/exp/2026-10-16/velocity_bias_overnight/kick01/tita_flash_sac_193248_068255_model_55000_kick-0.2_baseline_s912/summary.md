# tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "345106fa1e5e0f8a3b90b2b8db2ca4395557dd9a005199d9c9fb7939538580dc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 17.983318590596475,
  "max_drift_m": 17.983318590596475,
  "radial_IAE_m_s": 506.17947432951644,
  "signed_longitudinal_delta_m": 17.756786085889082,
  "tail_speed_mean_m_s": 0.32406481791609215,
  "tail_speed_rms_m_s": 0.32406482034643935,
  "tail_sensor_speed_mean_m_s": 0.3233641297928064,
  "tail_fk_speed_mean_m_s": 0.32335739076556325,
  "peak_tilt_rad": 0.173547097643304,
  "peak_wheel_torque_nm": 1.4762849807739258,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.455523035954684
}
```
