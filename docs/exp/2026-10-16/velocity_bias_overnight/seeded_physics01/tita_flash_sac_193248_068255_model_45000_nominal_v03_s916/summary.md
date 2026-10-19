# tita_flash_sac_193248_068255_model_45000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "cec4dd54ee9a674459c007402e288a18ea0c100ea52b9e29337874c70439d94b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0058784971780370164,
  "max_drift_m": 0.04389036456679752,
  "radial_IAE_m_s": 0.4774555595189199,
  "signed_longitudinal_delta_m": -0.005873783902393634,
  "tail_speed_mean_m_s": 4.01596899917923e-05,
  "tail_speed_rms_m_s": 4.0161531993522955e-05,
  "tail_sensor_speed_mean_m_s": 4.104058694402827e-05,
  "tail_fk_speed_mean_m_s": 3.855206239341332e-05,
  "peak_tilt_rad": 0.08079347813393589,
  "peak_wheel_torque_nm": 0.46634671092033386,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21209000064286038,
  "final_integral_m_s": -0.21209000064286038,
  "elapsed_wall_s": 9.41396886802977
}
```
