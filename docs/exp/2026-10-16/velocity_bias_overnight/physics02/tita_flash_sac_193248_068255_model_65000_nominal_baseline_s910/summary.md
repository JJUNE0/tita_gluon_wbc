# tita_flash_sac_193248_068255_model_65000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "737bd8e6710f0d3f88dcdfee25eb4df65ec45ef72b0e03582d86a12503af37a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.606092580964539,
  "max_drift_m": 2.606092580964539,
  "radial_IAE_m_s": 78.796001520777,
  "signed_longitudinal_delta_m": -2.6024211972016578,
  "tail_speed_mean_m_s": -0.042745820599654996,
  "tail_speed_rms_m_s": 0.042746281858885474,
  "tail_sensor_speed_mean_m_s": -0.04265885902880302,
  "tail_fk_speed_mean_m_s": -0.042653597701613664,
  "peak_tilt_rad": 0.029403256305726266,
  "peak_wheel_torque_nm": 0.04824557900428772,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.225811598997097
}
```
