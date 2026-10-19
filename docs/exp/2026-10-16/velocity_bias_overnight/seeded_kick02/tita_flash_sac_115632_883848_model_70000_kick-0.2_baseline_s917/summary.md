# tita_flash_sac_115632_883848_model_70000_kick-0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick-0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "58a73f2ccfc1e6331a7b6879b7ddde5ef3aeaa1ea082603dcf5ede580d918689",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.7080173669953975,
  "max_drift_m": 4.7080173669953975,
  "radial_IAE_m_s": 146.91127462718663,
  "signed_longitudinal_delta_m": -4.690469466636107,
  "tail_speed_mean_m_s": -0.07490800208916638,
  "tail_speed_rms_m_s": 0.07490812495994892,
  "tail_sensor_speed_mean_m_s": -0.0747461163830888,
  "tail_fk_speed_mean_m_s": -0.07474583192515084,
  "peak_tilt_rad": 0.027377395940726634,
  "peak_wheel_torque_nm": 1.779661774635315,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.942385539005045
}
```
