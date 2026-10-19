# tita_flash_sac_115632_883848_model_30000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "initial_physics_sha256": "5e11d34b051317fa1d935ba245ff9a56f6665304d898c37adbe851a47c6b2b82",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.050430197861952505,
  "max_drift_m": 0.10505200154908334,
  "radial_IAE_m_s": 3.021920024217536,
  "signed_longitudinal_delta_m": 0.05040901115586028,
  "tail_speed_mean_m_s": 5.658180049857762e-06,
  "tail_speed_rms_m_s": 6.5758731863754956e-06,
  "tail_sensor_speed_mean_m_s": 4.197832082026452e-06,
  "tail_fk_speed_mean_m_s": 6.292291340102957e-06,
  "peak_tilt_rad": 0.12619544120474457,
  "peak_wheel_torque_nm": 1.0901257991790771,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.529242963903109,
  "final_integral_m_s": 0.5292409298966902,
  "elapsed_wall_s": 12.316686953010503
}
```
