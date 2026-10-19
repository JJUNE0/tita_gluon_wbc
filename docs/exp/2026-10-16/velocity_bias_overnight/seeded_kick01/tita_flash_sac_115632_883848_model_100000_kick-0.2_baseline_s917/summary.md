# tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "00ee4ba35830207947442a9468c4688dd41e255bcdbe91f82943e31c22e1bb19",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.7553410807815775,
  "max_drift_m": 6.7553410807815775,
  "radial_IAE_m_s": 199.7158441988862,
  "signed_longitudinal_delta_m": 6.754988708388676,
  "tail_speed_mean_m_s": 0.11286281478936097,
  "tail_speed_rms_m_s": 0.11286385493703147,
  "tail_sensor_speed_mean_m_s": 0.11261824465177356,
  "tail_fk_speed_mean_m_s": 0.11261806948220766,
  "peak_tilt_rad": 0.08925971689890155,
  "peak_wheel_torque_nm": 2.0624117851257324,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.920284395979252
}
```
