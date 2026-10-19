# tita_flash_sac_115632_883848_model_70000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "6170438c1a70c48f6f4b69350fae107f5426ca78de8057432b9f0b49fc7aad5d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0016790682372691402,
  "max_drift_m": 0.023464144801578914,
  "radial_IAE_m_s": 0.14588038375123602,
  "signed_longitudinal_delta_m": -0.0014632056841470268,
  "tail_speed_mean_m_s": 7.447335462817186e-06,
  "tail_speed_rms_m_s": 8.419609910363442e-06,
  "tail_sensor_speed_mean_m_s": 7.394165675688159e-06,
  "tail_fk_speed_mean_m_s": 7.449757105541801e-06,
  "peak_tilt_rad": 0.04149300084719565,
  "peak_wheel_torque_nm": 0.31728288531303406,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12259511562635451,
  "final_integral_m_s": -0.12259511562635451,
  "elapsed_wall_s": 7.305668742978014
}
```
