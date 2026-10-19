# tita_flash_sac_193248_068255_model_60000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "7f50a10e0d9875f679348f5bfb9970fe68b0517abcb9d997c88fbd81ee6a248c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0036283918786025864,
  "max_drift_m": 0.005068159821326141,
  "radial_IAE_m_s": 0.23353586266449883,
  "signed_longitudinal_delta_m": 0.0036281780182560383,
  "tail_speed_mean_m_s": -7.759836260041085e-06,
  "tail_speed_rms_m_s": 7.855769239954302e-06,
  "tail_sensor_speed_mean_m_s": -1.540259550253144e-05,
  "tail_fk_speed_mean_m_s": -4.260545324072417e-06,
  "peak_tilt_rad": 0.033456241850948976,
  "peak_wheel_torque_nm": 0.09108906984329224,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04077759298422004,
  "final_integral_m_s": 0.0407843700795123,
  "elapsed_wall_s": 14.851627955038566
}
```
