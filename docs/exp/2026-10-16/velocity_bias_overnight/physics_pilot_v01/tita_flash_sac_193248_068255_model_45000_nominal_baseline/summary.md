# tita_flash_sac_193248_068255_model_45000_nominal_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "c0b8fa6c011a7620ef56f78c8c3006d990dd1bdb6aa6682ec4b2b6a82398b815",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.370034068591893,
  "max_drift_m": 8.370034068591893,
  "radial_IAE_m_s": 249.17570473534826,
  "signed_longitudinal_delta_m": -8.31554581805943,
  "tail_speed_mean_m_s": -0.14257535540987454,
  "tail_speed_rms_m_s": 0.14257786352573903,
  "tail_sensor_speed_mean_m_s": -0.142372840931267,
  "tail_fk_speed_mean_m_s": -0.14238692110686385,
  "peak_tilt_rad": 0.02626675985873117,
  "peak_wheel_torque_nm": 0.08150684833526611,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.053196081018541
}
```
