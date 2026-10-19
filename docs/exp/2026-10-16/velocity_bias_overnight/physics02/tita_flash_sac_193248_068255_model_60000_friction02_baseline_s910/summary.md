# tita_flash_sac_193248_068255_model_60000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 0.6426494436579567,
  "max_drift_m": 0.6426494436579567,
  "radial_IAE_m_s": 19.244053322861006,
  "signed_longitudinal_delta_m": 0.6419316146184645,
  "tail_speed_mean_m_s": 0.010717727818324004,
  "tail_speed_rms_m_s": 0.010717740166261645,
  "tail_sensor_speed_mean_m_s": 0.010705959509904564,
  "tail_fk_speed_mean_m_s": 0.010709730050789047,
  "peak_tilt_rad": 0.03363605348459853,
  "peak_wheel_torque_nm": 0.07875630259513855,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.173491348978132
}
```
