# tita_flash_sac_115632_883848_model_100000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "28d0b550b2c6d8886acef904b314eb6c37f8c1453ba7b77b2e7335811998d7a2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.004874730099517,
  "max_drift_m": 7.004874730099517,
  "radial_IAE_m_s": 213.54105387367372,
  "signed_longitudinal_delta_m": 7.0030353297545895,
  "tail_speed_mean_m_s": 0.11309515638225455,
  "tail_speed_rms_m_s": 0.11309641853344828,
  "tail_sensor_speed_mean_m_s": 0.11285002887712525,
  "tail_fk_speed_mean_m_s": 0.11284994901133141,
  "peak_tilt_rad": 0.09034333573905196,
  "peak_wheel_torque_nm": 0.32726043462753296,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.457502514007501
}
```
