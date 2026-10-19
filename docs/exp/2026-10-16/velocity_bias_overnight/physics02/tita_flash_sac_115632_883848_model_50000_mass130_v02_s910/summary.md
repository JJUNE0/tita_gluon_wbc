# tita_flash_sac_115632_883848_model_50000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "1a59aa57175bcc0057e4806670f746d323d4943c085900be324d4a7e172aa551",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.025766870847203457,
  "max_drift_m": 0.05418222489519297,
  "radial_IAE_m_s": 1.558149597530588,
  "signed_longitudinal_delta_m": -0.0257299899675235,
  "tail_speed_mean_m_s": -7.577808704675331e-07,
  "tail_speed_rms_m_s": 8.948539801972807e-07,
  "tail_sensor_speed_mean_m_s": -5.14779207403039e-07,
  "tail_fk_speed_mean_m_s": 1.9837368203071692e-07,
  "peak_tilt_rad": 0.165772929412914,
  "peak_wheel_torque_nm": 1.3003941774368286,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27174251545900396,
  "final_integral_m_s": -0.27174374593179024,
  "elapsed_wall_s": 12.133681473031174
}
```
