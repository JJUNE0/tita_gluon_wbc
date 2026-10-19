# tita_flash_sac_115632_883848_model_95000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
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
  "initial_physics_sha256": "46835e166625d2cb62d74cb56c926c223023b5b885c91dff545b5ec8eed7de6c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8321797751173432,
  "max_drift_m": 0.8321797751173432,
  "radial_IAE_m_s": 19.074539512472562,
  "signed_longitudinal_delta_m": 0.8314036724359194,
  "tail_speed_mean_m_s": 0.020147308466283202,
  "tail_speed_rms_m_s": 0.020212152343914255,
  "tail_sensor_speed_mean_m_s": 0.020104042450189017,
  "tail_fk_speed_mean_m_s": 0.020104099293256177,
  "peak_tilt_rad": 0.06373416363608975,
  "peak_wheel_torque_nm": 0.17630133032798767,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.04116810602136
}
```
