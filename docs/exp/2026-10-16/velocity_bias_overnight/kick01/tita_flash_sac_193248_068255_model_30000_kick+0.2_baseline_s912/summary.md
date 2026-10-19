# tita_flash_sac_193248_068255_model_30000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "67739eb934ab254fa33caf3f22177590faa07536824838fc653d17c4780b91c0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.057004703971428,
  "max_drift_m": 3.057004703971428,
  "radial_IAE_m_s": 95.85472681558387,
  "signed_longitudinal_delta_m": 3.05647472130756,
  "tail_speed_mean_m_s": 0.04838333556278318,
  "tail_speed_rms_m_s": 0.048383516261210374,
  "tail_sensor_speed_mean_m_s": 0.04827827306465572,
  "tail_fk_speed_mean_m_s": 0.048277022817412786,
  "peak_tilt_rad": 0.05522104415304252,
  "peak_wheel_torque_nm": 1.2383663654327393,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.103244332014583
}
```
