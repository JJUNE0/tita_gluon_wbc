# tita_flash_sac_193248_068255_model_30000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "002dac98bde16fb5e9a18d89768c35fc8ebe20221912c497be25b6f49d99d516",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009114958810994564,
  "max_drift_m": 0.01716268174724158,
  "radial_IAE_m_s": 0.529985717548542,
  "signed_longitudinal_delta_m": -0.009110460172992938,
  "tail_speed_mean_m_s": -1.9369604057122204e-05,
  "tail_speed_rms_m_s": 1.9375340511624184e-05,
  "tail_sensor_speed_mean_m_s": -1.9102577649613755e-05,
  "tail_fk_speed_mean_m_s": -1.9395166873095894e-05,
  "peak_tilt_rad": 0.02343245683734385,
  "peak_wheel_torque_nm": 0.37374812364578247,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10862127678685776,
  "final_integral_m_s": 0.10862127678685776,
  "elapsed_wall_s": 16.16317929100478
}
```
