# tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "16e8f2ab65730be3e666e1abe082e14d78007d924e13d9ba4817a4d5b2ce4735",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.3829689474859723,
  "max_drift_m": 3.3829689474859723,
  "radial_IAE_m_s": 100.96270956443921,
  "signed_longitudinal_delta_m": -3.377422960548906,
  "tail_speed_mean_m_s": -0.056466209364986926,
  "tail_speed_rms_m_s": 0.05646634414760873,
  "tail_sensor_speed_mean_m_s": -0.056344271626664874,
  "tail_fk_speed_mean_m_s": -0.05634435152394807,
  "peak_tilt_rad": 0.022198018166109668,
  "peak_wheel_torque_nm": 0.13188892602920532,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.314308442990296
}
```
