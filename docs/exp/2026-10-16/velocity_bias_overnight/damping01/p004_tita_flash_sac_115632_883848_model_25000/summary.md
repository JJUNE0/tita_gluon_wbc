# p004_tita_flash_sac_115632_883848_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p004_tita_flash_sac_115632_883848_model_25000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 0.5
    }
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
  "initial_physics_sha256": "6a7623095d59b3790ae881c3fb20f5d23e46e39e8f7925b4c03378dac73ab1e4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.15807841594885624,
  "max_drift_m": 0.2161736634689005,
  "radial_IAE_m_s": 9.205712797765406,
  "signed_longitudinal_delta_m": 0.1580726212290725,
  "tail_speed_mean_m_s": 0.00014183619775558643,
  "tail_speed_rms_m_s": 0.00014396415917704107,
  "tail_sensor_speed_mean_m_s": 0.00014114697419636941,
  "tail_fk_speed_mean_m_s": 0.00015029137707607088,
  "peak_tilt_rad": 0.13985636658553968,
  "peak_wheel_torque_nm": 1.4231293201446533,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 1.3419709098070696,
  "final_integral_m_s": 1.3417486991811554,
  "elapsed_wall_s": 12.720370755007025
}
```
