# tita_flash_sac_115632_883848_model_30000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "af1df7b948e879ab7c9931a58e175a984fb2d47f57702eecc5b81ad51ea1d328",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05370074287528783,
  "max_drift_m": 0.11796259467770202,
  "radial_IAE_m_s": 3.218920029115643,
  "signed_longitudinal_delta_m": 0.05368650164473677,
  "tail_speed_mean_m_s": 6.6486454170172685e-06,
  "tail_speed_rms_m_s": 1.4022685832046105e-05,
  "tail_sensor_speed_mean_m_s": 5.28425219118401e-06,
  "tail_fk_speed_mean_m_s": 7.158720458754108e-06,
  "peak_tilt_rad": 0.12852703277157773,
  "peak_wheel_torque_nm": 1.1351860761642456,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5644725905203621,
  "final_integral_m_s": 0.5644802227736851,
  "elapsed_wall_s": 12.308033750974573
}
```
