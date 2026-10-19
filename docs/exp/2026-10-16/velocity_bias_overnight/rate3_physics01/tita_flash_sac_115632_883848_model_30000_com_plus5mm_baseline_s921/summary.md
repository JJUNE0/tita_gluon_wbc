# tita_flash_sac_115632_883848_model_30000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "8efe62d4249b937f02454390812a175bec32abe9557761670daad0f967003943",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.127465434423474,
  "max_drift_m": 15.127465434423474,
  "radial_IAE_m_s": 456.9425024617795,
  "signed_longitudinal_delta_m": 15.106783258706862,
  "tail_speed_mean_m_s": 0.2501654843076026,
  "tail_speed_rms_m_s": 0.2501655092910457,
  "tail_sensor_speed_mean_m_s": 0.24962366257681948,
  "tail_fk_speed_mean_m_s": 0.24962218521282456,
  "peak_tilt_rad": 0.1275172073516464,
  "peak_wheel_torque_nm": 0.15551984310150146,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.893511684960686
}
```
