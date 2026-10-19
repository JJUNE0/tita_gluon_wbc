# tita_flash_sac_193248_068255_model_10000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "eab24717c21b8110a62f992be4a08bb7ae5638967ffb6153a3a5e516615ee635",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.6545304270879773,
  "max_drift_m": 1.6545304270879773,
  "radial_IAE_m_s": 50.62798552686391,
  "signed_longitudinal_delta_m": -1.647270269943862,
  "tail_speed_mean_m_s": -0.026639922337050672,
  "tail_speed_rms_m_s": 0.026757144292567408,
  "tail_sensor_speed_mean_m_s": -0.026574885424130744,
  "tail_fk_speed_mean_m_s": -0.02657723464742974,
  "peak_tilt_rad": 0.026870192728132205,
  "peak_wheel_torque_nm": 0.8922824263572693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.499448733986355
}
```
