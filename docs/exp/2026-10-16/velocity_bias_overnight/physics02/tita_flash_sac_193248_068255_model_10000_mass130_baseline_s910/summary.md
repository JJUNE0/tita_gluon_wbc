# tita_flash_sac_193248_068255_model_10000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "f8b260c29be8e666b45c3bcb76e9ad42fa6da6616e7771ddcdc955d5aebd5187",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.1881715865696125,
  "max_drift_m": 3.1881715865696125,
  "radial_IAE_m_s": 97.19533844288404,
  "signed_longitudinal_delta_m": -3.1769466488034412,
  "tail_speed_mean_m_s": -0.051610633967717895,
  "tail_speed_rms_m_s": 0.05161264870753956,
  "tail_sensor_speed_mean_m_s": -0.05149880079216619,
  "tail_fk_speed_mean_m_s": -0.05149797135461435,
  "peak_tilt_rad": 0.03477062809279263,
  "peak_wheel_torque_nm": 0.5662589073181152,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.041829360008705
}
```
