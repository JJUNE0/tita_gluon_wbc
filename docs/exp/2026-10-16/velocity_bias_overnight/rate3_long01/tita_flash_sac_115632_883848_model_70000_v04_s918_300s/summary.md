# tita_flash_sac_115632_883848_model_70000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "51a97a9f98a0d65a2894798cfa7a9a56c5d57a7a43781caa50989957b8ad21d7",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0022260119186793426,
  "max_drift_m": 0.023464137079765083,
  "radial_IAE_m_s": 0.6088423171382369,
  "signed_longitudinal_delta_m": -0.001699957659578477,
  "tail_speed_mean_m_s": -4.627369200442524e-06,
  "tail_speed_rms_m_s": 4.925582829623719e-06,
  "tail_sensor_speed_mean_m_s": -4.614824277080447e-06,
  "tail_fk_speed_mean_m_s": -4.765777506803993e-06,
  "peak_tilt_rad": 0.041493013097115394,
  "peak_wheel_torque_nm": 0.3172875940799713,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12318997564441171,
  "final_integral_m_s": -0.12318997564441171,
  "elapsed_wall_s": 55.065620277950075
}
```
