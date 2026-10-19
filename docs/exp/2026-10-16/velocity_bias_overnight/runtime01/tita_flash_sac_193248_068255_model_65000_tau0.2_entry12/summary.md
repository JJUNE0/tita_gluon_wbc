# tita_flash_sac_193248_068255_model_65000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
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
  "initial_physics_sha256": "ff698c5607c2c0c8604f83883d6d683ea9b28df2ecf598137df012cf6d0dba46",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018356533786029583,
  "max_drift_m": 0.030182583423969567,
  "radial_IAE_m_s": 1.1307510186018412,
  "signed_longitudinal_delta_m": -0.018349029112878626,
  "tail_speed_mean_m_s": 1.3133382174778484e-05,
  "tail_speed_rms_m_s": 1.3135097277110285e-05,
  "tail_sensor_speed_mean_m_s": 1.2651283181993691e-05,
  "tail_fk_speed_mean_m_s": 1.4064922740687945e-05,
  "peak_tilt_rad": 0.050957370514944644,
  "peak_wheel_torque_nm": 0.19641973078250885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18787195374016444,
  "final_integral_m_s": -0.18789941813508024,
  "elapsed_wall_s": 15.49917711300077
}
```
