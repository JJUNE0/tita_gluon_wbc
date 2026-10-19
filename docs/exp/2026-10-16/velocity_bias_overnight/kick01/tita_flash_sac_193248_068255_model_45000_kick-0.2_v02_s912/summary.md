# tita_flash_sac_193248_068255_model_45000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "0338938fe7acbe183f86375af3bfde2238197080c8eca272a42bd171794552fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.021391613746649208,
  "max_drift_m": 0.1164184574422057,
  "radial_IAE_m_s": 1.377497227032512,
  "signed_longitudinal_delta_m": -0.02139091914292006,
  "tail_speed_mean_m_s": 1.641974119372554e-05,
  "tail_speed_rms_m_s": 1.6420254181194513e-05,
  "tail_sensor_speed_mean_m_s": 1.7243257152269636e-05,
  "tail_fk_speed_mean_m_s": 1.4779648414040241e-05,
  "peak_tilt_rad": 0.15266518885593183,
  "peak_wheel_torque_nm": 1.9866210222244263,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.208135944884636,
  "final_integral_m_s": -0.20816480959505104,
  "elapsed_wall_s": 16.185950877028517
}
```
