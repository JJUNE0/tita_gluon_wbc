# tita_flash_sac_193248_068255_model_65000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "cfe71be0e9f3ae94e425ab0c9f19dac77b7598d423f70b23db12d49afea9f2c5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6107842142514994,
  "max_drift_m": 2.6107842142514994,
  "radial_IAE_m_s": 79.11573798912868,
  "signed_longitudinal_delta_m": -2.6070961860732873,
  "tail_speed_mean_m_s": -0.042723598657603515,
  "tail_speed_rms_m_s": 0.04272405782526881,
  "tail_sensor_speed_mean_m_s": -0.04263663188004024,
  "tail_fk_speed_mean_m_s": -0.04263128093174257,
  "peak_tilt_rad": 0.028345512171257692,
  "peak_wheel_torque_nm": 0.04309159517288208,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.228242636017967
}
```
