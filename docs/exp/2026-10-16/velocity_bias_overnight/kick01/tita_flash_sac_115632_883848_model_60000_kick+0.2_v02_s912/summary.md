# tita_flash_sac_115632_883848_model_60000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "3ed1b14ef0116d572f2266cc6a9a69aec0aee5b2b240da5d1e531e12d2101a13",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005744844553934767,
  "max_drift_m": 0.0734938192964928,
  "radial_IAE_m_s": 0.41109371696682767,
  "signed_longitudinal_delta_m": 0.005744838410838842,
  "tail_speed_mean_m_s": -1.0975440746368629e-05,
  "tail_speed_rms_m_s": 1.1178397531843073e-05,
  "tail_sensor_speed_mean_m_s": -1.0996144999116154e-05,
  "tail_fk_speed_mean_m_s": -8.900778165004005e-06,
  "peak_tilt_rad": 0.09529745332238138,
  "peak_wheel_torque_nm": 2.2367310523986816,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.04755380620749902,
  "final_integral_m_s": 0.04756312344532881,
  "elapsed_wall_s": 14.934533305000514
}
```
