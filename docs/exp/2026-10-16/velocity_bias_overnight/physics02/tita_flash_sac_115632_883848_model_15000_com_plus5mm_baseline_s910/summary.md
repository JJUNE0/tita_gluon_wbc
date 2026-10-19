# tita_flash_sac_115632_883848_model_15000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "d376259e507c1f42b949094f5a31732a0e186b2de65616c49e8dd68aea38ff5b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.860786809855204,
  "max_drift_m": 6.860786809855204,
  "radial_IAE_m_s": 204.76448750147404,
  "signed_longitudinal_delta_m": -6.849415745155526,
  "tail_speed_mean_m_s": -0.11502372711464068,
  "tail_speed_rms_m_s": 0.1150404906838487,
  "tail_sensor_speed_mean_m_s": -0.114921218651794,
  "tail_fk_speed_mean_m_s": -0.11485170436238083,
  "peak_tilt_rad": 0.06557092930062125,
  "peak_wheel_torque_nm": 2.0950767993927,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.203649503993802
}
```
