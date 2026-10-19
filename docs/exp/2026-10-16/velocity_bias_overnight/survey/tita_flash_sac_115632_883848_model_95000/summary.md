# tita_flash_sac_115632_883848_model_95000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "828a8fafa94e4db7e71325e819102eef4424ab91dc43889d0eaca074c8250254",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.2618081929656144,
  "max_drift_m": 1.2618081929656144,
  "radial_IAE_m_s": 32.905262358407725,
  "signed_longitudinal_delta_m": 1.2610625098536585,
  "tail_speed_mean_m_s": 0.026440120119187446,
  "tail_speed_rms_m_s": 0.026474094942601223,
  "tail_sensor_speed_mean_m_s": 0.02638337589445509,
  "tail_fk_speed_mean_m_s": 0.02638333688149017,
  "peak_tilt_rad": 0.06473469345200078,
  "peak_wheel_torque_nm": 0.114362433552742,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.3855832779663615
}
```
