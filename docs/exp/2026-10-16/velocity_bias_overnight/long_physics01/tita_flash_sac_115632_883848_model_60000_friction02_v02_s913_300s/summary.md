# tita_flash_sac_115632_883848_model_60000_friction02_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_friction02_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "320c1433872100d9a89952b28db46fac857c641a1c6d24bb8d6278d2ddeb2762",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.002863014357008198,
  "max_drift_m": 0.0078082598860458536,
  "radial_IAE_m_s": 0.8534113880049075,
  "signed_longitudinal_delta_m": 0.0027782361101585462,
  "tail_speed_mean_m_s": 7.635710379256822e-07,
  "tail_speed_rms_m_s": 7.658462339216866e-07,
  "tail_sensor_speed_mean_m_s": -3.457288963928585e-05,
  "tail_fk_speed_mean_m_s": 3.038889186936143e-08,
  "peak_tilt_rad": 0.06149666934956999,
  "peak_wheel_torque_nm": 0.1828148066997528,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04235392811247099,
  "final_integral_m_s": 0.04235411295266335,
  "elapsed_wall_s": 52.41510916501284
}
```
