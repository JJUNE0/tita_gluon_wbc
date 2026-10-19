# tita_flash_sac_193248_068255_model_45000_baseline_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_baseline_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "81719af94f0f0d6ea89f765c5c33fc2e15783ac890264e85db0058f7b049a520",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 18.344329776915753,
  "max_drift_m": 26.783897548135148,
  "radial_IAE_m_s": 5207.79771857792,
  "signed_longitudinal_delta_m": -2.600714660383658,
  "tail_speed_mean_m_s": -0.20629387510664626,
  "tail_speed_rms_m_s": 0.20629420066348408,
  "tail_sensor_speed_mean_m_s": -0.20586012797785852,
  "tail_fk_speed_mean_m_s": -0.20593790892527827,
  "peak_tilt_rad": 0.039688262588903456,
  "peak_wheel_torque_nm": 0.19217121601104736,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 51.145144876034465
}
```
