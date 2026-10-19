# tita_flash_sac_115632_883848_model_5000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "20858b84d804ab31e1cd334d0b38917005a7e867f598005a1abb5dd9302de7a4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.02154807611305,
  "max_drift_m": 10.02154807611305,
  "radial_IAE_m_s": 304.18291561713556,
  "signed_longitudinal_delta_m": -9.203166874590899,
  "tail_speed_mean_m_s": -0.1691564658411996,
  "tail_speed_rms_m_s": 0.17038759925028454,
  "tail_sensor_speed_mean_m_s": -0.16840532609725986,
  "tail_fk_speed_mean_m_s": -0.16830977841964656,
  "peak_tilt_rad": 0.07381744388002742,
  "peak_wheel_torque_nm": 3.884765625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.679021305055358
}
```
