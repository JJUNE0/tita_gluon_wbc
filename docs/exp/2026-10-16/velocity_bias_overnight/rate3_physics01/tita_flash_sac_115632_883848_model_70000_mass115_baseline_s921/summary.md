# tita_flash_sac_115632_883848_model_70000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "c8f624f3b5d56e076dc5c0b823a8751b553259d1e44d86db53b8f110a9eb1bfe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.30405207410221,
  "max_drift_m": 8.30405207410221,
  "radial_IAE_m_s": 248.81919677011143,
  "signed_longitudinal_delta_m": -8.287919916872351,
  "tail_speed_mean_m_s": -0.1385332396110212,
  "tail_speed_rms_m_s": 0.138533259821906,
  "tail_sensor_speed_mean_m_s": -0.13823452039557074,
  "tail_fk_speed_mean_m_s": -0.1382346804629648,
  "peak_tilt_rad": 0.016455552288648614,
  "peak_wheel_torque_nm": 0.19334381818771362,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.68854001298314
}
```
