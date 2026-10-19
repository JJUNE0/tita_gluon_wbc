# tita_flash_sac_115632_883848_model_100000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "2a4361942ac69c3892a89d6be2d17d6837c8a7d8c12bf6a37d6c3073c9af9ab8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.0716528541698045,
  "max_drift_m": 7.0716528541698045,
  "radial_IAE_m_s": 219.00382457420122,
  "signed_longitudinal_delta_m": 7.0695929123994965,
  "tail_speed_mean_m_s": 0.11264938281686046,
  "tail_speed_rms_m_s": 0.11265024657672185,
  "tail_sensor_speed_mean_m_s": 0.11240530012887873,
  "tail_fk_speed_mean_m_s": 0.11240505784180393,
  "peak_tilt_rad": 0.10477188259097492,
  "peak_wheel_torque_nm": 1.970129370689392,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.784518221975304
}
```
