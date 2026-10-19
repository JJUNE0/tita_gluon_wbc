# tita_flash_sac_115632_883848_model_10000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
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
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "d7556c4271eeee87de3e5e7a7140859699c494f176c7a1c2ffd2e8bd1d30faf3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.5006808319882743,
  "max_drift_m": 1.5006808319882743,
  "radial_IAE_m_s": 46.251078587091065,
  "signed_longitudinal_delta_m": -1.500674567546208,
  "tail_speed_mean_m_s": -0.024001813826392986,
  "tail_speed_rms_m_s": 0.024002885238357065,
  "tail_sensor_speed_mean_m_s": -0.02395017241542745,
  "tail_fk_speed_mean_m_s": -0.023950423206495767,
  "peak_tilt_rad": 0.08131856552702521,
  "peak_wheel_torque_nm": 1.8540256023406982,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.134022225975059
}
```
