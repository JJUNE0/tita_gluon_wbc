# tita_flash_sac_115632_883848_model_100000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "dd1e77eb0c024033ef534b10412b7d2e7bfc65e2dcccb420d7876bf900f3fb7d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.009346605154105,
  "max_drift_m": 7.009346605154105,
  "radial_IAE_m_s": 213.7309600577822,
  "signed_longitudinal_delta_m": 7.0072239506674245,
  "tail_speed_mean_m_s": 0.11311786607975938,
  "tail_speed_rms_m_s": 0.11311915132790885,
  "tail_sensor_speed_mean_m_s": 0.11287269105135353,
  "tail_fk_speed_mean_m_s": 0.11287261394307338,
  "peak_tilt_rad": 0.09040469797020667,
  "peak_wheel_torque_nm": 0.32377350330352783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.645002247998491
}
```
