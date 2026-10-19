# tita_flash_sac_193248_068255_model_30000_nominal_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_nominal_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "3f2f1105bf577a63faa630cab51de587908027acec9ac255603fcaf108e74c99",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.9342480008754186,
  "max_drift_m": 2.9342480008754186,
  "radial_IAE_m_s": 88.30997991672129,
  "signed_longitudinal_delta_m": 2.933686780352106,
  "tail_speed_mean_m_s": 0.04853008427859301,
  "tail_speed_rms_m_s": 0.04853028175640581,
  "tail_sensor_speed_mean_m_s": 0.048424605362417945,
  "tail_fk_speed_mean_m_s": 0.04842337368020857,
  "peak_tilt_rad": 0.019881780091460355,
  "peak_wheel_torque_nm": 0.1527242362499237,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.549103984958492
}
```
