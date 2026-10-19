# tita_flash_sac_115632_883848_model_35000_nominal_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_nominal_baseline_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "0ef6ab55bbc18928cd0e6406efd8eeca222366e346705c2f6672eeabf109e2f5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.793470468523896,
  "max_drift_m": 13.793470468523896,
  "radial_IAE_m_s": 410.4014572584789,
  "signed_longitudinal_delta_m": 13.79266079217846,
  "tail_speed_mean_m_s": 0.23248634864668394,
  "tail_speed_rms_m_s": 0.2324863514723553,
  "tail_sensor_speed_mean_m_s": 0.23198341783898058,
  "tail_fk_speed_mean_m_s": 0.23198148261810084,
  "peak_tilt_rad": 0.14051811531579572,
  "peak_wheel_torque_nm": 0.8839691877365112,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.307463183999062
}
```
