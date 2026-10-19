# tita_flash_sac_115632_883848_model_90000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "490aa176539308101f85ea81b163de6171981f0e03aa7317480add478833c27c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860030871607746,
  "max_drift_m": 6.860030871607746,
  "radial_IAE_m_s": 205.70242551316693,
  "signed_longitudinal_delta_m": -6.857573536831608,
  "tail_speed_mean_m_s": -0.11439651934676866,
  "tail_speed_rms_m_s": 0.11439652117570549,
  "tail_sensor_speed_mean_m_s": -0.11415089181662173,
  "tail_fk_speed_mean_m_s": -0.1141507411959639,
  "peak_tilt_rad": 0.07611497862696348,
  "peak_wheel_torque_nm": 0.7648981213569641,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.023961747006979
}
```
