# tita_flash_sac_115632_883848_model_70000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "3e747914673725abca4e0970d059433bfdcf2d9172f0c2cc41c24b6525e734ef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009792383479373369,
  "max_drift_m": 0.019193918446467704,
  "radial_IAE_m_s": 0.6099476341417868,
  "signed_longitudinal_delta_m": -0.009781996647328222,
  "tail_speed_mean_m_s": 1.094832067439587e-05,
  "tail_speed_rms_m_s": 1.1229503885283113e-05,
  "tail_sensor_speed_mean_m_s": 1.0897346667521106e-05,
  "tail_fk_speed_mean_m_s": 1.0839703610196052e-05,
  "peak_tilt_rad": 0.03339806377465737,
  "peak_wheel_torque_nm": 0.15091346204280853,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.08954029157224758,
  "final_integral_m_s": -0.08954029157224758,
  "elapsed_wall_s": 10.291900698968675
}
```
