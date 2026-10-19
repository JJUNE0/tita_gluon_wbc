# tita_flash_sac_115632_883848_model_20000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "427ff07db9c32c5bf6d399ac5e6ec264b6c8dc8993aa24598f2e3b00a5d826c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.392942679019592,
  "max_drift_m": 14.392942679019592,
  "radial_IAE_m_s": 433.8785012977258,
  "signed_longitudinal_delta_m": 13.945284998686816,
  "tail_speed_mean_m_s": 0.24545406899198213,
  "tail_speed_rms_m_s": 0.2454540690308539,
  "tail_sensor_speed_mean_m_s": 0.24492576597752647,
  "tail_fk_speed_mean_m_s": 0.2448953674003027,
  "peak_tilt_rad": 0.17106120984580953,
  "peak_wheel_torque_nm": 0.36233317852020264,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.982924398034811
}
```
