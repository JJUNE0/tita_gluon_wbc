# tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "239e55ee2aa6584aa5cef34c09122d0deed268fe7a2e3ffd5c1d18d58c074b10",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.747491322233478,
  "max_drift_m": 6.747491322233478,
  "radial_IAE_m_s": 199.39004437800133,
  "signed_longitudinal_delta_m": 6.746947345146785,
  "tail_speed_mean_m_s": 0.1128191368222755,
  "tail_speed_rms_m_s": 0.11282013877968307,
  "tail_sensor_speed_mean_m_s": 0.11257466815933302,
  "tail_fk_speed_mean_m_s": 0.1125744760466907,
  "peak_tilt_rad": 0.0891464008991052,
  "peak_wheel_torque_nm": 2.0630197525024414,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.032043054990936
}
```
