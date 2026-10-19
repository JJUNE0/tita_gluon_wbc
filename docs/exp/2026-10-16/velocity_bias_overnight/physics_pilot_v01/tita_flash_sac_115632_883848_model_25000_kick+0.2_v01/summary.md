# tita_flash_sac_115632_883848_model_25000_kick+0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_v01",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
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
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "7b256aa98a16b4b7feaae40c3db4b1513420c2633813a497dc374629ae5a215f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.2272237214817599,
  "max_drift_m": 0.28005359349721265,
  "radial_IAE_m_s": 13.434382280416132,
  "signed_longitudinal_delta_m": 0.2272132401229964,
  "tail_speed_mean_m_s": 8.61242726494431e-05,
  "tail_speed_rms_m_s": 8.671271954153063e-05,
  "tail_sensor_speed_mean_m_s": 8.866298677392459e-05,
  "tail_fk_speed_mean_m_s": 9.97916213070168e-05,
  "peak_tilt_rad": 0.13853012599867087,
  "peak_wheel_torque_nm": 4.309868812561035,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3722732394413544,
  "final_integral_m_s": 1.3721014392240363,
  "elapsed_wall_s": 4.715405650960747
}
```
