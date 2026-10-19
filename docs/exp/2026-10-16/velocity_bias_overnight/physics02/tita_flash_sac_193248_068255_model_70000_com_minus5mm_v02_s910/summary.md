# tita_flash_sac_193248_068255_model_70000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "8f8550e1dffbb870d2048ef4b7dc79bca6357d911381bf0ab163e48c52c56bbe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0015356046586895962,
  "max_drift_m": 0.008790515322258477,
  "radial_IAE_m_s": 0.05101063200643905,
  "signed_longitudinal_delta_m": 0.0015336563834425544,
  "tail_speed_mean_m_s": 3.180301805862176e-05,
  "tail_speed_rms_m_s": 3.180446670114138e-05,
  "tail_sensor_speed_mean_m_s": 3.186978847898501e-05,
  "tail_fk_speed_mean_m_s": 3.160912355719632e-05,
  "peak_tilt_rad": 0.07708609306626224,
  "peak_wheel_torque_nm": 0.21535471081733704,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.012454816478761881,
  "final_integral_m_s": 0.012392675293191314,
  "elapsed_wall_s": 22.106274919002317
}
```
