# tita_flash_sac_115632_883848_model_50000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d5b7c981c4c4cd5375fd5513ec12f02c7abada4ca21df8727729faf1d0e31e7c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_50000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_50000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "f5f168ea9590afd458db6be3c8fb9e89977091d89c192c3ab60cfdaafd25fa0f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.004241731668162069,
  "max_drift_m": 0.010601127139411073,
  "radial_IAE_m_s": 0.20031798981212207,
  "signed_longitudinal_delta_m": 0.003013430231777071,
  "tail_speed_mean_m_s": -2.8234624992840953e-05,
  "tail_speed_rms_m_s": 3.4697508623041135e-05,
  "tail_sensor_speed_mean_m_s": 0.00011557777410147776,
  "tail_fk_speed_mean_m_s": 9.14386419710188e-06,
  "peak_tilt_rad": 0.04025033063427075,
  "peak_wheel_torque_nm": 0.244724839925766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.022448189735942196,
  "final_integral_m_s": 0.022441167121298358,
  "elapsed_wall_s": 12.861265305022243
}
```
