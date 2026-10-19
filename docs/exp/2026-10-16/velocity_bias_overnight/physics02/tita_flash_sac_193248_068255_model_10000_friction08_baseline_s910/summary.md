# tita_flash_sac_193248_068255_model_10000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "initial_physics_sha256": "4ec37a130816d7d6d4be2b6de65588fbcac49b09ba5db1f45f9d874915947e5a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.6435734069111669,
  "max_drift_m": 0.6435734069111669,
  "radial_IAE_m_s": 12.544871763623313,
  "signed_longitudinal_delta_m": 0.5311071703025629,
  "tail_speed_mean_m_s": -0.03163987125125842,
  "tail_speed_rms_m_s": 0.032165412775812564,
  "tail_sensor_speed_mean_m_s": -0.031778086384608016,
  "tail_fk_speed_mean_m_s": -0.031638135302054345,
  "peak_tilt_rad": 0.034767556936701194,
  "peak_wheel_torque_nm": 0.8300175666809082,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.223523557011504
}
```
