# tita_flash_sac_193248_068255_model_75000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "5515d07fe3f92aec1f76a639b8296bb9d3cd0bd488107caa1729ed42d5f4ac2c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.143139469953358,
  "max_drift_m": 13.143139469953358,
  "radial_IAE_m_s": 395.8554187716635,
  "signed_longitudinal_delta_m": -10.853103414686945,
  "tail_speed_mean_m_s": -0.26236901979064126,
  "tail_speed_rms_m_s": 0.26243156900488807,
  "tail_sensor_speed_mean_m_s": -0.2620394915619522,
  "tail_fk_speed_mean_m_s": -0.2620777152019322,
  "peak_tilt_rad": 0.024309764598882788,
  "peak_wheel_torque_nm": 0.11281096935272217,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.716005783993751
}
```
