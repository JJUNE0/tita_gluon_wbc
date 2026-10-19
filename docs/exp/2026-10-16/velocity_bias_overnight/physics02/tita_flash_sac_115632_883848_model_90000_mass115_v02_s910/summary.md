# tita_flash_sac_115632_883848_model_90000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "80a3aa29a2a7f08a80a9f9c89397affece829996cc3ab551f347c632c7cd8268",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010815571195994326,
  "max_drift_m": 0.01912499042393026,
  "radial_IAE_m_s": 0.6579670483128508,
  "signed_longitudinal_delta_m": -0.010814943360425783,
  "tail_speed_mean_m_s": 8.737648341735905e-07,
  "tail_speed_rms_m_s": 1.447498215192166e-06,
  "tail_sensor_speed_mean_m_s": 8.289945462706985e-07,
  "tail_fk_speed_mean_m_s": 1.063635223410843e-06,
  "peak_tilt_rad": 0.08858775064138369,
  "peak_wheel_torque_nm": 0.9185592532157898,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.11500868070637278,
  "final_integral_m_s": -0.1150149415358363,
  "elapsed_wall_s": 17.383672759053297
}
```
