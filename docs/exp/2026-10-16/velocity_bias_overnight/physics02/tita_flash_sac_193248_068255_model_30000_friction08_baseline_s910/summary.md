# tita_flash_sac_193248_068255_model_30000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "2ba90a74aac663a632b172cb58cb33a544ad97112e1471a8afb2f807f02ca5cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.9498527231191654,
  "max_drift_m": 2.9498527231191654,
  "radial_IAE_m_s": 88.58020102852905,
  "signed_longitudinal_delta_m": 2.9495464360226853,
  "tail_speed_mean_m_s": 0.04902321505713185,
  "tail_speed_rms_m_s": 0.04902348813481319,
  "tail_sensor_speed_mean_m_s": 0.04892561755332991,
  "tail_fk_speed_mean_m_s": 0.048924565226238614,
  "peak_tilt_rad": 0.018716040573707238,
  "peak_wheel_torque_nm": 0.15806792676448822,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.17678383900784
}
```
