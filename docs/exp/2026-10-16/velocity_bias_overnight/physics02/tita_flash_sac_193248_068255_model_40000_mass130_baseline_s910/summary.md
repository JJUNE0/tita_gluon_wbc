# tita_flash_sac_193248_068255_model_40000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "c7a90137e909b74caa2b06ce292fe41eea5de6451b3062ece473b539366d2be1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.0914998865028505,
  "max_drift_m": 4.0914998865028505,
  "radial_IAE_m_s": 122.55902787685977,
  "signed_longitudinal_delta_m": -4.090542111137837,
  "tail_speed_mean_m_s": -0.06821378203657812,
  "tail_speed_rms_m_s": 0.06821381939254137,
  "tail_sensor_speed_mean_m_s": -0.06806739044162663,
  "tail_fk_speed_mean_m_s": -0.0680669209149335,
  "peak_tilt_rad": 0.11717386150466291,
  "peak_wheel_torque_nm": 0.2907533347606659,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.40534908499103
}
```
