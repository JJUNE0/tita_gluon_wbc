# tita_flash_sac_115632_883848_model_100000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": false,
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
  "initial_physics_sha256": "626296b4ffb97098a43630e215acaed163e20e00083f6a26407ba03114d18331",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 33.227971186197095,
  "max_drift_m": 33.227971186197095,
  "radial_IAE_m_s": 5046.207506371908,
  "signed_longitudinal_delta_m": 32.74468241478315,
  "tail_speed_mean_m_s": 0.11025855679418464,
  "tail_speed_rms_m_s": 0.1102585568188242,
  "tail_sensor_speed_mean_m_s": 0.11001975189772026,
  "tail_fk_speed_mean_m_s": 0.1100192364509178,
  "peak_tilt_rad": 0.08961135033280443,
  "peak_wheel_torque_nm": 0.3863818943500519,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 45.17173973302124
}
```
