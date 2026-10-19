# tita_flash_sac_115632_883848_model_70000_friction02_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction02_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
    },
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "54dfe1f28b3dfaba7f2f4d7b3a52014bdf7f9c3b95c1f844b6af5aa39fdc1ef8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0008284349768334958,
  "max_drift_m": 0.023978485251245314,
  "radial_IAE_m_s": 0.09665486750308527,
  "signed_longitudinal_delta_m": 0.00038684386331093917,
  "tail_speed_mean_m_s": -1.4028310108290851e-06,
  "tail_speed_rms_m_s": 2.389610776474665e-06,
  "tail_sensor_speed_mean_m_s": -1.3911182523449542e-06,
  "tail_fk_speed_mean_m_s": -1.534114946015619e-06,
  "peak_tilt_rad": 0.03845452365673285,
  "peak_wheel_torque_nm": 0.35274770855903625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12256662347545322,
  "final_integral_m_s": -0.12256662347545322,
  "elapsed_wall_s": 10.215283385012299
}
```
