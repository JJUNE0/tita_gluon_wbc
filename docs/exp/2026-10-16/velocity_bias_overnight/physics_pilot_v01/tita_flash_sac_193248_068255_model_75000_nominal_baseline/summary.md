# tita_flash_sac_193248_068255_model_75000_nominal_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.0,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
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
  "initial_physics_sha256": "fbc5df3efdc8ffb7939436a546f14b0be6b79b66d55f9ffcac9b0c65b6911729",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.143139432392061,
  "max_drift_m": 13.143139432392061,
  "radial_IAE_m_s": 395.8554225504072,
  "signed_longitudinal_delta_m": -10.853103022981562,
  "tail_speed_mean_m_s": -0.26236901911427724,
  "tail_speed_rms_m_s": 0.26243156811606516,
  "tail_sensor_speed_mean_m_s": -0.26203949020688816,
  "tail_fk_speed_mean_m_s": -0.26207771497243537,
  "peak_tilt_rad": 0.024309767322425513,
  "peak_wheel_torque_nm": 0.11281442642211914,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.667263486015145
}
```
