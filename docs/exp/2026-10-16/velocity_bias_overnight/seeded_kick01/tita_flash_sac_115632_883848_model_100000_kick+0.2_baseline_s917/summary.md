# tita_flash_sac_115632_883848_model_100000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "d6e602e2a55f60f04449cba9a789a6c77b84659b4ea55fd24b0573baa45d76e7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.078792354073965,
  "max_drift_m": 7.078792354073965,
  "radial_IAE_m_s": 219.30067788274897,
  "signed_longitudinal_delta_m": 7.077071134818621,
  "tail_speed_mean_m_s": 0.1126896141329465,
  "tail_speed_rms_m_s": 0.1126905108656835,
  "tail_sensor_speed_mean_m_s": 0.11244543746225603,
  "tail_fk_speed_mean_m_s": 0.11244521119973408,
  "peak_tilt_rad": 0.10484598788615429,
  "peak_wheel_torque_nm": 1.9589816331863403,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.244611389993224
}
```
