# tita_flash_sac_193248_068255_model_25000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "a48a9e930ff54f3c5772a252bab75b973274b90e182890185f6e5e6f36d7b822",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.561546934785589,
  "max_drift_m": 3.561546934785589,
  "radial_IAE_m_s": 112.61548714105844,
  "signed_longitudinal_delta_m": 3.557099488095157,
  "tail_speed_mean_m_s": 0.053393438414840524,
  "tail_speed_rms_m_s": 0.05340654674550619,
  "tail_sensor_speed_mean_m_s": 0.05327872665587985,
  "tail_fk_speed_mean_m_s": 0.05327895749764016,
  "peak_tilt_rad": 0.10953102601919418,
  "peak_wheel_torque_nm": 0.14736133813858032,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.33770682400791
}
```
