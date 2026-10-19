# tita_flash_sac_115632_883848_model_5000_baseline_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_baseline_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "e67b65d9dd572b37c5fc984eba9110379400d67230f825ed965cb5fca0f159f4",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 30.585109510478063,
  "max_drift_m": 36.75246548544812,
  "radial_IAE_m_s": 19619.51293585599,
  "signed_longitudinal_delta_m": -15.611664649906846,
  "tail_speed_mean_m_s": -0.1687377022809179,
  "tail_speed_rms_m_s": 0.16996388315752087,
  "tail_sensor_speed_mean_m_s": -0.1682291041066897,
  "tail_fk_speed_mean_m_s": -0.16793968924898414,
  "peak_tilt_rad": 0.0736931450307341,
  "peak_wheel_torque_nm": 3.89255690574646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 137.98523374804063
}
```
