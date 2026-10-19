# tita_flash_sac_115632_883848_model_25000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "5295976788d620026a502acbf3646d5d6dd247dafd261219331bf4178a743342",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0943443708190309,
  "max_drift_m": 0.2590593982537559,
  "radial_IAE_m_s": 5.140540531035224,
  "signed_longitudinal_delta_m": 0.09432712695124335,
  "tail_speed_mean_m_s": 0.000357872943229213,
  "tail_speed_rms_m_s": 0.000363790727267886,
  "tail_sensor_speed_mean_m_s": 0.0003563935714594974,
  "tail_fk_speed_mean_m_s": 0.00036572165065889645,
  "peak_tilt_rad": 0.17486302204188253,
  "peak_wheel_torque_nm": 3.712308883666992,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.343234376121527,
  "final_integral_m_s": 1.343234376121527,
  "elapsed_wall_s": 11.13279322697781
}
```
