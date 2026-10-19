# tita_flash_sac_193248_068255_model_70000_friction02_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction02_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "25cdfc04dd900fdb05f1dd5e10a02bda8b1f330fd719ca65f8f86f6124431f53",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.145097355692791,
  "max_drift_m": 4.145097355692791,
  "radial_IAE_m_s": 124.65941175936723,
  "signed_longitudinal_delta_m": 4.140396207277407,
  "tail_speed_mean_m_s": 0.0682969360538378,
  "tail_speed_rms_m_s": 0.06829752001867445,
  "tail_sensor_speed_mean_m_s": 0.06814881672157584,
  "tail_fk_speed_mean_m_s": 0.06814809935960213,
  "peak_tilt_rad": 0.08932380106461846,
  "peak_wheel_torque_nm": 0.1113138496875763,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.254209232982248
}
```
