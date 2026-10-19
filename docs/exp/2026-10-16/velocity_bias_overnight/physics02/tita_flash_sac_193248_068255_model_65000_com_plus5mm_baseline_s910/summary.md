# tita_flash_sac_193248_068255_model_65000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "e789a74e4803823925a288403ad28bc0c38b70f779ddbce290455253f82103f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8107116924000511,
  "max_drift_m": 0.8107116924000511,
  "radial_IAE_m_s": 25.158564460962637,
  "signed_longitudinal_delta_m": -0.809979315441,
  "tail_speed_mean_m_s": -0.012556663464287632,
  "tail_speed_rms_m_s": 0.012560127869645131,
  "tail_sensor_speed_mean_m_s": -0.01252930851215972,
  "tail_fk_speed_mean_m_s": -0.012526434699526811,
  "peak_tilt_rad": 0.03383452081614058,
  "peak_wheel_torque_nm": 0.05308609455823898,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.312473079015035
}
```
