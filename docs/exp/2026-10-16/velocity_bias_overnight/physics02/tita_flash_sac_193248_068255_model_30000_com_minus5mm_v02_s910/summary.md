# tita_flash_sac_193248_068255_model_30000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "initial_physics_sha256": "22635d31619a10fe35f7bd37afa31faac0d0442de8592b2a92c0f4da805c2c1b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006018009722644415,
  "max_drift_m": 0.010293619768361888,
  "radial_IAE_m_s": 0.3652447531940719,
  "signed_longitudinal_delta_m": 0.006015063880412067,
  "tail_speed_mean_m_s": -1.4265289586931883e-06,
  "tail_speed_rms_m_s": 1.4307468229320583e-06,
  "tail_sensor_speed_mean_m_s": -1.1501029777358875e-06,
  "tail_fk_speed_mean_m_s": -1.5200170612482848e-06,
  "peak_tilt_rad": 0.01215778251366717,
  "peak_wheel_torque_nm": 0.22518384456634521,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.06162795400672408,
  "final_integral_m_s": 0.06163043136346009,
  "elapsed_wall_s": 19.403044042992406
}
```
