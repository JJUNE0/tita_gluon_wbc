# tita_flash_sac_115632_883848_model_30000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "4f3bb36c39be0ef484e20ed2678c80f214f62c4f602f23a048321f7e29dc415f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.932471998771057,
  "max_drift_m": 13.932471998771057,
  "radial_IAE_m_s": 418.2908637017483,
  "signed_longitudinal_delta_m": 13.91145748832956,
  "tail_speed_mean_m_s": 0.23134154725788972,
  "tail_speed_rms_m_s": 0.23134163950767514,
  "tail_sensor_speed_mean_m_s": 0.2308404291891971,
  "tail_fk_speed_mean_m_s": 0.2308388418646732,
  "peak_tilt_rad": 0.1267979366596872,
  "peak_wheel_torque_nm": 1.5466179847717285,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.038155950023793
}
```
