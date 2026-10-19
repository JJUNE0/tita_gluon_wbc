# tita_flash_sac_115632_883848_model_50000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
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
  "checkpoint_sha256": "d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c",
  "onnx_sha256": "0128f5783513e86a2d0cfbc67ed5d02260d017356909fa01ccf0635c03248873",
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
  "initial_physics_sha256": "ee3751db2ab4807246b1cc3aba6d175fbf7161aeccdc4924dc50e14f6493d7a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0016955071901511181,
  "max_drift_m": 0.00402190026903984,
  "radial_IAE_m_s": 0.10051156179977569,
  "signed_longitudinal_delta_m": 0.0014751978454223596,
  "tail_speed_mean_m_s": -3.6249318809314327e-07,
  "tail_speed_rms_m_s": 2.007168820188851e-06,
  "tail_sensor_speed_mean_m_s": -1.7575592001787388e-07,
  "tail_fk_speed_mean_m_s": 2.2391558747528085e-06,
  "peak_tilt_rad": 0.04181549943421037,
  "peak_wheel_torque_nm": 0.3274041414260864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.021380762515745756,
  "final_integral_m_s": 0.021379736690226667,
  "elapsed_wall_s": 11.20888383599231
}
```
