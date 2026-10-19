# tita_flash_sac_193248_068255_model_45000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "da0b37876c9d66d19dcfa9fac1a625c6228c6218686762922014a5ade9ac50be",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020109324316779045,
  "max_drift_m": 0.037347238101805125,
  "radial_IAE_m_s": 1.2437844220530825,
  "signed_longitudinal_delta_m": -0.020106132484483022,
  "tail_speed_mean_m_s": 1.666724070331453e-05,
  "tail_speed_rms_m_s": 1.666778463419182e-05,
  "tail_sensor_speed_mean_m_s": 1.7537393078891026e-05,
  "tail_fk_speed_mean_m_s": 1.5065577505741955e-05,
  "peak_tilt_rad": 0.0812300571591047,
  "peak_wheel_torque_nm": 0.49003922939300537,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21001113744776267,
  "final_integral_m_s": -0.21004081880123865,
  "elapsed_wall_s": 16.424420442956034
}
```
