# tita_flash_sac_115632_883848_model_70000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "6685417ee36b466696c28b393473f498b39ae777578dbf9987565e776f4a324f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011886051333453712,
  "max_drift_m": 0.021257599166596978,
  "radial_IAE_m_s": 0.7208000722241394,
  "signed_longitudinal_delta_m": -0.011859515854805576,
  "tail_speed_mean_m_s": 2.1257950104160037e-06,
  "tail_speed_rms_m_s": 2.8711082488413576e-06,
  "tail_sensor_speed_mean_m_s": 2.086690967797932e-06,
  "tail_fk_speed_mean_m_s": 2.13827991223669e-06,
  "peak_tilt_rad": 0.04101569301886476,
  "peak_wheel_torque_nm": 0.35070663690567017,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12259874079097258,
  "final_integral_m_s": -0.12259850824310009,
  "elapsed_wall_s": 12.552198352001142
}
```
