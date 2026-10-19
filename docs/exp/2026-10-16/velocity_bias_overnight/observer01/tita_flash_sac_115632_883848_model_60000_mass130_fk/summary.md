# tita_flash_sac_115632_883848_model_60000_mass130_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_fk",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "d393bd92f9cdf47131e0ad8f9193a9875947ef831a33d735176e1feca2e48122",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.037267463363778085,
  "max_drift_m": 0.0742171279661298,
  "radial_IAE_m_s": 2.395418569154167,
  "signed_longitudinal_delta_m": -0.03726379127879672,
  "tail_speed_mean_m_s": 0.0001236426594841606,
  "tail_speed_rms_m_s": 0.016493673302256526,
  "tail_sensor_speed_mean_m_s": 0.0004268084380966609,
  "tail_fk_speed_mean_m_s": -7.281528032952186e-05,
  "peak_tilt_rad": 0.18280737347071163,
  "peak_wheel_torque_nm": 5.444761276245117,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.44018264629077597,
  "final_integral_m_s": -0.4179012448070739,
  "elapsed_wall_s": 14.70694431202719
}
```
