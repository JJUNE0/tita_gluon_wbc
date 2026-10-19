# tita_flash_sac_115632_883848_model_5000_com-0.005_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com-0.005_baseline",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": -0.005
    },
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "31beae326f0d556d7c3e765e7fdfa18a5a4f0e97ffe23868f0c1b243a5c00dc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.807474669627938,
  "max_drift_m": 10.807474669627938,
  "radial_IAE_m_s": 327.2828938203604,
  "signed_longitudinal_delta_m": -10.267324131505847,
  "tail_speed_mean_m_s": -0.1821080726484927,
  "tail_speed_rms_m_s": 0.18308071550964855,
  "tail_sensor_speed_mean_m_s": -0.1797882407225579,
  "tail_fk_speed_mean_m_s": -0.18105699476079667,
  "peak_tilt_rad": 0.08120072773758058,
  "peak_wheel_torque_nm": 3.8844778537750244,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.462675364979077
}
```
