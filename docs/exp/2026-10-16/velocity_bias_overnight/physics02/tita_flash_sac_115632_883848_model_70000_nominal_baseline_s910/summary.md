# tita_flash_sac_115632_883848_model_70000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "6685417ee36b466696c28b393473f498b39ae777578dbf9987565e776f4a324f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.5119091042968344,
  "max_drift_m": 4.5119091042968344,
  "radial_IAE_m_s": 135.36399545273588,
  "signed_longitudinal_delta_m": -4.497432630722109,
  "tail_speed_mean_m_s": -0.0748849070974367,
  "tail_speed_rms_m_s": 0.07488501754571439,
  "tail_sensor_speed_mean_m_s": -0.07472302031826974,
  "tail_fk_speed_mean_m_s": -0.07472278221697361,
  "peak_tilt_rad": 0.01939113693562544,
  "peak_wheel_torque_nm": 0.12340843677520752,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.112408443994354
}
```
