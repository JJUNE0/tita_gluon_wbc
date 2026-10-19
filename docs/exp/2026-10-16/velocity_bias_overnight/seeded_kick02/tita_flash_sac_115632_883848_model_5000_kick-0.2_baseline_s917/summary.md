# tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "1c7466b0931c77cfeb9376742c740605948a92ff2ff2563b03a480164769bbd6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.099185830600181,
  "max_drift_m": 10.099185830600181,
  "radial_IAE_m_s": 307.58010977736257,
  "signed_longitudinal_delta_m": -9.58067061979899,
  "tail_speed_mean_m_s": -0.16910498994692938,
  "tail_speed_rms_m_s": 0.17033437381925143,
  "tail_sensor_speed_mean_m_s": -0.16850278024190554,
  "tail_fk_speed_mean_m_s": -0.1682591438490632,
  "peak_tilt_rad": 0.10009306672024332,
  "peak_wheel_torque_nm": 5.353917121887207,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.949960064026527
}
```
