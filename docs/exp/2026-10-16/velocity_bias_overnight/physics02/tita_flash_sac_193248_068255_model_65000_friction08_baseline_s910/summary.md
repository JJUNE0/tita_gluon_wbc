# tita_flash_sac_193248_068255_model_65000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "initial_physics_sha256": "cd281ae4b412b510f1e3b82e512c2e3342f34869abcbcf0e5f737bceacf50eba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.886937559024351,
  "max_drift_m": 2.886937559024351,
  "radial_IAE_m_s": 86.87937296077546,
  "signed_longitudinal_delta_m": -2.886596938311225,
  "tail_speed_mean_m_s": -0.04772898807115642,
  "tail_speed_rms_m_s": 0.047729232476956825,
  "tail_sensor_speed_mean_m_s": -0.047651226431061865,
  "tail_fk_speed_mean_m_s": -0.04764941333936299,
  "peak_tilt_rad": 0.03014917056188282,
  "peak_wheel_torque_nm": 0.05838344991207123,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.97493340499932
}
```
