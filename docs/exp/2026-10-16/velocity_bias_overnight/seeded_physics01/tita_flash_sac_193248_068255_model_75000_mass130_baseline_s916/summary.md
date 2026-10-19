# tita_flash_sac_193248_068255_model_75000_mass130_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "d7324f92d782fbbeb5de0b6b90d6be3eaca5fc61da04d75db4aa0539800d4720",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.47035924490563,
  "max_drift_m": 15.47035924490563,
  "radial_IAE_m_s": 477.97638520924545,
  "signed_longitudinal_delta_m": -14.044716111322073,
  "tail_speed_mean_m_s": -0.2994692249989093,
  "tail_speed_rms_m_s": 0.2995679184854693,
  "tail_sensor_speed_mean_m_s": -0.29871711077397683,
  "tail_fk_speed_mean_m_s": -0.2987409982997336,
  "peak_tilt_rad": 0.08562659069667045,
  "peak_wheel_torque_nm": 0.6799173355102539,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.947294025972951
}
```
