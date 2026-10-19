# tita_flash_sac_193248_068255_model_5000_mass115_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass115_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "f3438036097cf98fe19c42b931402cdc368394a9d4ee941cfc066c1fd0d6f965",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.940583312832832,
  "max_drift_m": 3.940583312832832,
  "radial_IAE_m_s": 127.29708498361367,
  "signed_longitudinal_delta_m": -3.7057325036109203,
  "tail_speed_mean_m_s": -0.06358494975338794,
  "tail_speed_rms_m_s": 0.06359265176318209,
  "tail_sensor_speed_mean_m_s": -0.06376880626362418,
  "tail_fk_speed_mean_m_s": -0.0638899325563417,
  "peak_tilt_rad": 0.06536083238903179,
  "peak_wheel_torque_nm": 2.0691635608673096,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.11415241000941
}
```
