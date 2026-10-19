# tita_flash_sac_115632_883848_model_100000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
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
  "initial_physics_sha256": "1e86e2de162518ca37e240477bc35c926864e1c4ae30cce713d8b251fd15b454",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.955597136044524,
  "max_drift_m": 7.955597136044524,
  "radial_IAE_m_s": 241.26027537307715,
  "signed_longitudinal_delta_m": 7.953258716324657,
  "tail_speed_mean_m_s": 0.12975301090544267,
  "tail_speed_rms_m_s": 0.12975454482511647,
  "tail_sensor_speed_mean_m_s": 0.12949317760427742,
  "tail_fk_speed_mean_m_s": 0.1294748388973741,
  "peak_tilt_rad": 0.0894800910020741,
  "peak_wheel_torque_nm": 0.44851216673851013,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.166423438000493
}
```
