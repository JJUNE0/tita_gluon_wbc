# tita_flash_sac_193248_068255_model_45000_nominal_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.01931046724774255,
  "max_drift_m": 0.05738088827149393,
  "radial_IAE_m_s": 1.210703037530382,
  "signed_longitudinal_delta_m": -0.019308789691388165,
  "tail_speed_mean_m_s": 1.6946073788641938e-05,
  "tail_speed_rms_m_s": 1.694655252075789e-05,
  "tail_sensor_speed_mean_m_s": 1.7872967097828788e-05,
  "tail_fk_speed_mean_m_s": 1.5390339166162576e-05,
  "peak_tilt_rad": 0.1014418344502197,
  "peak_wheel_torque_nm": 0.9297633767127991,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2119518667778749,
  "final_integral_m_s": -0.21198219499069404,
  "elapsed_wall_s": 5.0807462349766865
}
```
