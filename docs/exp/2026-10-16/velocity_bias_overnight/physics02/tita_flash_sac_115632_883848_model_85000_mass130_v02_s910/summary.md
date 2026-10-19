# tita_flash_sac_115632_883848_model_85000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "0423ae5935ec55a4ab0b84d1e8dd19439684b7c029379a649e6d0cff88e1e29a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04178913831189588,
  "max_drift_m": 0.05688113132121017,
  "radial_IAE_m_s": 2.4159444195649495,
  "signed_longitudinal_delta_m": -0.041769410732265325,
  "tail_speed_mean_m_s": -3.96598914268304e-05,
  "tail_speed_rms_m_s": 0.005608930984476473,
  "tail_sensor_speed_mean_m_s": 0.00035546026755380316,
  "tail_fk_speed_mean_m_s": 3.391752669628411e-05,
  "peak_tilt_rad": 0.13738052132116318,
  "peak_wheel_torque_nm": 1.6356219053268433,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3987220182193055,
  "final_integral_m_s": -0.40653285441231835,
  "elapsed_wall_s": 19.299714269000106
}
```
