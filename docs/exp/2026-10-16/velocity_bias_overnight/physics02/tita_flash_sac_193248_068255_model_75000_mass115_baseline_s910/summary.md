# tita_flash_sac_193248_068255_model_75000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
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
  "initial_physics_sha256": "b08a0747dc4734b4631bd5c2fab8c754c1bb9984707334fcca73bb60aa188434",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.431179532994411,
  "max_drift_m": 13.431179532994411,
  "radial_IAE_m_s": 408.3326598471802,
  "signed_longitudinal_delta_m": -11.528287363180757,
  "tail_speed_mean_m_s": -0.27469211023356765,
  "tail_speed_rms_m_s": 0.27492379907895087,
  "tail_sensor_speed_mean_m_s": -0.2743197095417885,
  "tail_fk_speed_mean_m_s": -0.27434905114881547,
  "peak_tilt_rad": 0.06808376358710566,
  "peak_wheel_torque_nm": 0.5819233059883118,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.916476187005173
}
```
