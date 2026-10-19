# tita_flash_sac_115632_883848_model_50000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "68651f9b495c72f785b959c059d1e2e251e18ad127460ad0a487f52b002ae242",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0019108237218245544,
  "max_drift_m": 0.0035280525074772263,
  "radial_IAE_m_s": 0.10878279547827222,
  "signed_longitudinal_delta_m": 0.0010587302085506717,
  "tail_speed_mean_m_s": -2.505650163665692e-06,
  "tail_speed_rms_m_s": 2.6219252214921932e-06,
  "tail_sensor_speed_mean_m_s": -1.7461895563292704e-06,
  "tail_fk_speed_mean_m_s": 5.39393968805811e-07,
  "peak_tilt_rad": 0.041555251814963556,
  "peak_wheel_torque_nm": 0.2909243404865265,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.02134939576731945,
  "final_integral_m_s": 0.02135038787371126,
  "elapsed_wall_s": 12.511667539016344
}
```
