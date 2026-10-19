# tita_flash_sac_115632_883848_model_100000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "bf6e040e34a6d8b811ddbfbc25fc3c63f4e8ce579469f58079595e07140fea17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.949146932480809,
  "max_drift_m": 5.949146932480809,
  "radial_IAE_m_s": 180.8453847154439,
  "signed_longitudinal_delta_m": 5.949101326875898,
  "tail_speed_mean_m_s": 0.09619806174931576,
  "tail_speed_rms_m_s": 0.09620001867295377,
  "tail_sensor_speed_mean_m_s": 0.09599249063342562,
  "tail_fk_speed_mean_m_s": 0.09598962592181712,
  "peak_tilt_rad": 0.08917195856779636,
  "peak_wheel_torque_nm": 0.3537277281284332,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.720065993024036
}
```
