# tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "c7abb82a5a457b325adb86c54c1cdf6c12f057091ca9891022d7fc94c402b64f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.142848893488072,
  "max_drift_m": 13.142848893488072,
  "radial_IAE_m_s": 395.11335102771034,
  "signed_longitudinal_delta_m": -11.247325822952357,
  "tail_speed_mean_m_s": -0.2577609065485961,
  "tail_speed_rms_m_s": 0.2578355867784155,
  "tail_sensor_speed_mean_m_s": -0.2574528754980579,
  "tail_fk_speed_mean_m_s": -0.25748381756065813,
  "peak_tilt_rad": 0.048255029446969244,
  "peak_wheel_torque_nm": 1.6125478744506836,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.565504828991834
}
```
