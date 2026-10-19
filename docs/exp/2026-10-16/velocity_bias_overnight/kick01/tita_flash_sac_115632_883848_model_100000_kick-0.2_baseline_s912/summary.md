# tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "bfe5755e59d9190ba4d27d4878a2fbf0ac973dc4fc7c0eed032d81b60cee9f7c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.7474912486408645,
  "max_drift_m": 6.7474912486408645,
  "radial_IAE_m_s": 199.3900285488672,
  "signed_longitudinal_delta_m": 6.746947261036871,
  "tail_speed_mean_m_s": 0.11281915312389529,
  "tail_speed_rms_m_s": 0.11282015509100309,
  "tail_sensor_speed_mean_m_s": 0.1125746868223874,
  "tail_fk_speed_mean_m_s": 0.11257449187473613,
  "peak_tilt_rad": 0.08914643630547014,
  "peak_wheel_torque_nm": 2.0630271434783936,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.769594063982368
}
```
