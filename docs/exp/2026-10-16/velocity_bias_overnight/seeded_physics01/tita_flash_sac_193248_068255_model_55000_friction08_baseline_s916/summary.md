# tita_flash_sac_193248_068255_model_55000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "3aa168e7d97b644b7b86a35e92a72ed2e36e9144c437227cdf1f22418ffd7876",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 18.340724874160415,
  "max_drift_m": 18.340724874160415,
  "radial_IAE_m_s": 526.9992183920001,
  "signed_longitudinal_delta_m": 18.177274965893716,
  "tail_speed_mean_m_s": 0.32406634105305687,
  "tail_speed_rms_m_s": 0.3240663433240137,
  "tail_sensor_speed_mean_m_s": 0.3233656458648476,
  "tail_fk_speed_mean_m_s": 0.32335891063777344,
  "peak_tilt_rad": 0.17354687111761913,
  "peak_wheel_torque_nm": 0.2589768171310425,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.91191791696474
}
```
