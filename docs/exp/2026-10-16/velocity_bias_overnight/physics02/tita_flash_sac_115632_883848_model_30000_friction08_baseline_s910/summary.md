# tita_flash_sac_115632_883848_model_30000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "af1df7b948e879ab7c9931a58e175a984fb2d47f57702eecc5b81ad51ea1d328",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.098480740731485,
  "max_drift_m": 14.098480740731485,
  "radial_IAE_m_s": 427.77379976627685,
  "signed_longitudinal_delta_m": 14.086451467217048,
  "tail_speed_mean_m_s": 0.23139182615383355,
  "tail_speed_rms_m_s": 0.23139194094711477,
  "tail_sensor_speed_mean_m_s": 0.23089057469759586,
  "tail_fk_speed_mean_m_s": 0.23088901853502067,
  "peak_tilt_rad": 0.128562918149852,
  "peak_wheel_torque_nm": 0.1339932680130005,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.02622296003392
}
```
