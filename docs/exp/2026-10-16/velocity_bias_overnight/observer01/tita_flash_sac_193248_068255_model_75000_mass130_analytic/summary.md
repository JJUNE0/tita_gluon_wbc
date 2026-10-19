# tita_flash_sac_193248_068255_model_75000_mass130_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_analytic",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
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
  "initial_physics_sha256": "b3f53a534f120fd37a6c8036018151e0c70ffbf7304d7afb3ddae5242ad8e3aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04998803321347852,
  "max_drift_m": 0.13633738032887885,
  "radial_IAE_m_s": 2.9232693645561216,
  "signed_longitudinal_delta_m": -0.04998530370829129,
  "tail_speed_mean_m_s": -6.228113256231274e-05,
  "tail_speed_rms_m_s": 0.004693313029960497,
  "tail_sensor_speed_mean_m_s": -0.0003093372540973948,
  "tail_fk_speed_mean_m_s": -1.8190244624194616e-05,
  "peak_tilt_rad": 0.2565025056316066,
  "peak_wheel_torque_nm": 3.1476778984069824,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5120325568891306,
  "final_integral_m_s": -0.5053921620383928,
  "elapsed_wall_s": 14.757948338985443
}
```
