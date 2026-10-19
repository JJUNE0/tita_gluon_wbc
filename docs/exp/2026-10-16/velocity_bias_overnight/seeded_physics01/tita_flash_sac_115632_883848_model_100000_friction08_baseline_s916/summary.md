# tita_flash_sac_115632_883848_model_100000_friction08_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_friction08_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "62fae31a4733691028693dafae47ddffa093729e8a4a376316c3862eabd1ef62",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.009347245962892,
  "max_drift_m": 7.009347245962892,
  "radial_IAE_m_s": 213.73098189588558,
  "signed_longitudinal_delta_m": 7.0072245924324585,
  "tail_speed_mean_m_s": 0.113117881145708,
  "tail_speed_rms_m_s": 0.11311916631257433,
  "tail_sensor_speed_mean_m_s": 0.11287270555087148,
  "tail_fk_speed_mean_m_s": 0.1128726283942792,
  "peak_tilt_rad": 0.09040473866732257,
  "peak_wheel_torque_nm": 0.3237723112106323,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.627893423021305
}
```
