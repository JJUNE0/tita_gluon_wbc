# tita_flash_sac_193248_068255_model_40000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "4cb502b3767ae39fbd598ac138086f205efc5ed3e828c6110f22c1aa35e979b9",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.028058880879155236,
  "max_drift_m": 0.04373576495047795,
  "radial_IAE_m_s": 7.889092753252642,
  "signed_longitudinal_delta_m": 0.02805548724911895,
  "tail_speed_mean_m_s": 3.210669324210926e-06,
  "tail_speed_rms_m_s": 3.2433815665244324e-06,
  "tail_sensor_speed_mean_m_s": 3.515100498241256e-06,
  "tail_fk_speed_mean_m_s": 3.0623963899113084e-06,
  "peak_tilt_rad": 0.10845429977152121,
  "peak_wheel_torque_nm": 0.8908487558364868,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29328051917840864,
  "final_integral_m_s": 0.29327444329679303,
  "elapsed_wall_s": 78.24618303100578
}
```
