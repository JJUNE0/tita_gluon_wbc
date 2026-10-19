# tita_flash_sac_193248_068255_model_5000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "3777e810fa1deaca1eb648c4968d7987aee33398d3c11d60ee5f6763a3bf1aae",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.572787087755035,
  "max_drift_m": 1.7098337637899532,
  "radial_IAE_m_s": 335.58902300697423,
  "signed_longitudinal_delta_m": -0.45530300456134754,
  "tail_speed_mean_m_s": -0.0398709706111379,
  "tail_speed_rms_m_s": 0.03987098656132221,
  "tail_sensor_speed_mean_m_s": -0.040299683915978206,
  "tail_fk_speed_mean_m_s": -0.040665722985641375,
  "peak_tilt_rad": 0.09274148808136662,
  "peak_wheel_torque_nm": 0.8814106583595276,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.28565457800869
}
```
