# tita_flash_sac_115632_883848_model_70000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "18361f28d6839b7441612aa75af4744218437e26bb094215f82320b1f402b7ea",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011921198346631488,
  "max_drift_m": 0.021626966222083408,
  "radial_IAE_m_s": 0.724800257054359,
  "signed_longitudinal_delta_m": -0.011895477995761376,
  "tail_speed_mean_m_s": 3.0962234126492985e-06,
  "tail_speed_rms_m_s": 3.099673660973471e-06,
  "tail_sensor_speed_mean_m_s": 3.042259955169774e-06,
  "tail_fk_speed_mean_m_s": 3.125063418029716e-06,
  "peak_tilt_rad": 0.04222900643526817,
  "peak_wheel_torque_nm": 0.3501766324043274,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12330058598783566,
  "final_integral_m_s": -0.12330735814414606,
  "elapsed_wall_s": 11.849247956008185
}
```
