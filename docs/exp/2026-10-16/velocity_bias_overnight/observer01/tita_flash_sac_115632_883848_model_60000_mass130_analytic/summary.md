# tita_flash_sac_115632_883848_model_60000_mass130_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass130_analytic",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
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
  "final_drift_m": 0.036803537757797294,
  "max_drift_m": 0.07420625066793851,
  "radial_IAE_m_s": 2.3812831200796976,
  "signed_longitudinal_delta_m": -0.0368027318142401,
  "tail_speed_mean_m_s": 9.734790990579588e-05,
  "tail_speed_rms_m_s": 0.007034569910535088,
  "tail_sensor_speed_mean_m_s": -0.0005215301621347401,
  "tail_fk_speed_mean_m_s": 8.81226429685308e-05,
  "peak_tilt_rad": 0.1818972508912553,
  "peak_wheel_torque_nm": 3.2479894161224365,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3965851323263004,
  "final_integral_m_s": -0.3970903834873525,
  "elapsed_wall_s": 15.988735236984212
}
```
