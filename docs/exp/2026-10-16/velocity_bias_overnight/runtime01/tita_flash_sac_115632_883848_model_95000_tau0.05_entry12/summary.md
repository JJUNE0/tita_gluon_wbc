# tita_flash_sac_115632_883848_model_95000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "8a03d41db92000995cdb289d12df37b505522d7f3a55405a181a3f9de81c56c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008273523456970864,
  "max_drift_m": 0.008273523456970864,
  "radial_IAE_m_s": 0.3339979720947171,
  "signed_longitudinal_delta_m": 0.008267720064233403,
  "tail_speed_mean_m_s": 9.709233840080442e-05,
  "tail_speed_rms_m_s": 9.817506847649668e-05,
  "tail_sensor_speed_mean_m_s": 9.680760222282491e-05,
  "tail_fk_speed_mean_m_s": 9.74009972287962e-05,
  "peak_tilt_rad": 0.06097732332396055,
  "peak_wheel_torque_nm": 0.1858997642993927,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08201152504932528,
  "final_integral_m_s": 0.08179794477833865,
  "elapsed_wall_s": 6.104730975988787
}
```
