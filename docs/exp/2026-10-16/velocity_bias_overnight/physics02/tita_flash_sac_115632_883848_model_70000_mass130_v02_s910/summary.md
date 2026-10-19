# tita_flash_sac_115632_883848_model_70000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "0a9c7c48ced8e1b2a0cf5ba991a47a3f4e4617255a56e2927f2fc269721a6093",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03381731970684971,
  "max_drift_m": 0.06470935496212481,
  "radial_IAE_m_s": 2.0591605020362085,
  "signed_longitudinal_delta_m": -0.03380851490474391,
  "tail_speed_mean_m_s": 9.867738900637898e-06,
  "tail_speed_rms_m_s": 9.871905964590573e-06,
  "tail_sensor_speed_mean_m_s": 9.60992091804079e-06,
  "tail_fk_speed_mean_m_s": 8.970940671347298e-06,
  "peak_tilt_rad": 0.1365250014319428,
  "peak_wheel_torque_nm": 1.1336469650268555,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.35750677937159003,
  "final_integral_m_s": -0.357525662616199,
  "elapsed_wall_s": 12.294894391030539
}
```
