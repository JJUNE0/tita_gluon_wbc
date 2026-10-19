# tita_flash_sac_115632_883848_model_75000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
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
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "0b26e4b7a2df55664ac275921ce0b9f6b356b2cb4a25ff2843fb6e2277e92dc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04714921674830168,
  "max_drift_m": 0.10266729413744251,
  "radial_IAE_m_s": 2.869917865664701,
  "signed_longitudinal_delta_m": -0.04714540064515547,
  "tail_speed_mean_m_s": 8.060306559695473e-06,
  "tail_speed_rms_m_s": 8.069424930399826e-06,
  "tail_sensor_speed_mean_m_s": 7.98599639061e-06,
  "tail_fk_speed_mean_m_s": 8.12441861729188e-06,
  "peak_tilt_rad": 0.17538300541830742,
  "peak_wheel_torque_nm": 2.1737165451049805,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4992583495665563,
  "final_integral_m_s": -0.4992738202766756,
  "elapsed_wall_s": 13.95390604401473
}
```
