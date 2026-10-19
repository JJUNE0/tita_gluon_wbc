# p000_tita_flash_sac_115632_883848_model_60000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p000_tita_flash_sac_115632_883848_model_60000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "kp": -2.0,
      "ki": 0.5,
      "tau": 0.1,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 1.0,
      "ramp": 1.5
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "490180ebc26fe7e12ee32c42daa5e84b7f4bbbccfcbaf6c05a14c248d084e6b4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09389627073114307,
  "max_drift_m": 0.11567870397921816,
  "radial_IAE_m_s": 5.64747343104156,
  "signed_longitudinal_delta_m": 0.09389547671720234,
  "tail_speed_mean_m_s": -0.00013867021844389755,
  "tail_speed_rms_m_s": 0.0001472722490112142,
  "tail_sensor_speed_mean_m_s": -0.0001382888012082106,
  "tail_fk_speed_mean_m_s": -0.00013626978388047472,
  "peak_tilt_rad": 0.07321941931509324,
  "peak_wheel_torque_nm": 0.13411633670330048,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.047227044700317224,
  "final_integral_m_s": 0.04704183359160816,
  "elapsed_wall_s": 5.3694139039726
}
```
