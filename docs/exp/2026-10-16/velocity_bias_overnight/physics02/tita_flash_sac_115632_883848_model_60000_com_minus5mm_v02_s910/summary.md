# tita_flash_sac_115632_883848_model_60000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "3888d208460ff4242191c0ca6cce1df5fafbc93252a6c1e2cabd3cea3ed4d148",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0005974559314648133,
  "max_drift_m": 0.0016195122064573257,
  "radial_IAE_m_s": 0.026153476909282998,
  "signed_longitudinal_delta_m": 6.582762862064773e-05,
  "tail_speed_mean_m_s": 1.2890789265992171e-05,
  "tail_speed_rms_m_s": 1.3315449936245653e-05,
  "tail_sensor_speed_mean_m_s": 1.2647466324114585e-05,
  "tail_fk_speed_mean_m_s": 1.4995153501220447e-05,
  "peak_tilt_rad": 0.06810611650025011,
  "peak_wheel_torque_nm": 0.15425671637058258,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0021754966054603054,
  "final_integral_m_s": 0.002145505983079718,
  "elapsed_wall_s": 17.382516220968682
}
```
