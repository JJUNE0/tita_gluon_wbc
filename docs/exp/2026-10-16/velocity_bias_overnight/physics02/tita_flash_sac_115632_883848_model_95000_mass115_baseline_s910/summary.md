# tita_flash_sac_115632_883848_model_95000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "initial_physics_sha256": "a9146b08e843643fb20bf3a97361aa1b7c08fae0ead649e0425db1df054b60f7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.829040555367145,
  "max_drift_m": 9.829040555367145,
  "radial_IAE_m_s": 295.5919428167994,
  "signed_longitudinal_delta_m": -9.794885186387146,
  "tail_speed_mean_m_s": -0.1622404103561018,
  "tail_speed_rms_m_s": 0.1622425729133744,
  "tail_sensor_speed_mean_m_s": -0.16190100879424046,
  "tail_fk_speed_mean_m_s": -0.16190186374832938,
  "peak_tilt_rad": 0.039782297004551825,
  "peak_wheel_torque_nm": 0.22777611017227173,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.238299161021132
}
```
