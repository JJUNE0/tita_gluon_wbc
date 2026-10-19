# tita_flash_sac_193248_068255_model_70000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "4efe6c997ecfbcc4f991be32cc756130b28f5790637a57f5d7d67744acf30210",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00263474129131496,
  "max_drift_m": 0.0158311724242375,
  "radial_IAE_m_s": 0.16802891474324838,
  "signed_longitudinal_delta_m": 0.0025815411701418834,
  "tail_speed_mean_m_s": 2.1627041650305727e-05,
  "tail_speed_rms_m_s": 0.005151665233656187,
  "tail_sensor_speed_mean_m_s": 0.0005058098189136771,
  "tail_fk_speed_mean_m_s": 2.8349362851529706e-05,
  "peak_tilt_rad": 0.07881177059153588,
  "peak_wheel_torque_nm": 1.2290403842926025,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2117227794002773,
  "final_integral_m_s": 0.10447335945717243,
  "elapsed_wall_s": 4.4482824630104005
}
```
