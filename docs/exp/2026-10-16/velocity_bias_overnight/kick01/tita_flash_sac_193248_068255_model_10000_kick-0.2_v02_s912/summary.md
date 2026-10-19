# tita_flash_sac_193248_068255_model_10000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "11f5b361ef849baf096ea386ef715f4a57a5efc9d0dfbf39105668a7243926cd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008895714190483243,
  "max_drift_m": 0.04591466910815924,
  "radial_IAE_m_s": 0.47724739818064454,
  "signed_longitudinal_delta_m": 0.008521685280616925,
  "tail_speed_mean_m_s": 5.503601118682252e-05,
  "tail_speed_rms_m_s": 5.506626376063508e-05,
  "tail_sensor_speed_mean_m_s": 6.847715620968247e-05,
  "tail_fk_speed_mean_m_s": 7.514067545009978e-05,
  "peak_tilt_rad": 0.08814966962320181,
  "peak_wheel_torque_nm": 3.8682990074157715,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12898687971863043,
  "final_integral_m_s": 0.12884342468592305,
  "elapsed_wall_s": 14.094746627029963
}
```
