# tita_flash_sac_193248_068255_model_65000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "3b5f120fd8dceb8a7fbf9ee8fd90864ceb977d79dbed204eb9b1f1e78db89d2f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030588180003181017,
  "max_drift_m": 0.04386498385068774,
  "radial_IAE_m_s": 1.8478741966365735,
  "signed_longitudinal_delta_m": -0.030579358030167203,
  "tail_speed_mean_m_s": 6.69307838423674e-06,
  "tail_speed_rms_m_s": 6.693954703231248e-06,
  "tail_sensor_speed_mean_m_s": 6.264682101212981e-06,
  "tail_fk_speed_mean_m_s": 7.331750793607019e-06,
  "peak_tilt_rad": 0.05889592036461422,
  "peak_wheel_torque_nm": 0.38095903396606445,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3137483061818142,
  "final_integral_m_s": -0.31376269655781236,
  "elapsed_wall_s": 15.04387615097221
}
```
