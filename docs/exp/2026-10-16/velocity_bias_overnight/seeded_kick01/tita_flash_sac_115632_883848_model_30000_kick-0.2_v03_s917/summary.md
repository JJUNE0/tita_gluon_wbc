# tita_flash_sac_115632_883848_model_30000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "4f3bb36c39be0ef484e20ed2678c80f214f62c4f602f23a048321f7e29dc415f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03739399843997403,
  "max_drift_m": 0.05465511906677647,
  "radial_IAE_m_s": 2.2471158085453142,
  "signed_longitudinal_delta_m": -0.03736969749323511,
  "tail_speed_mean_m_s": -1.5661904151201728e-05,
  "tail_speed_rms_m_s": 2.9173064840727826e-05,
  "tail_sensor_speed_mean_m_s": -1.690788119264959e-05,
  "tail_fk_speed_mean_m_s": -1.5164621871577454e-05,
  "peak_tilt_rad": 0.1267979366596872,
  "peak_wheel_torque_nm": 1.309615969657898,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5635759350981834,
  "final_integral_m_s": 0.5635759350981834,
  "elapsed_wall_s": 8.74903541902313
}
```
