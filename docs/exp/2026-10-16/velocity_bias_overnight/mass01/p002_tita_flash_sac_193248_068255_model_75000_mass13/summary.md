# p002_tita_flash_sac_193248_068255_model_75000_mass13

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p002_tita_flash_sac_193248_068255_model_75000_mass13",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 5.0,
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
  "final_drift_m": 0.10215615123506241,
  "max_drift_m": 0.1418360081019331,
  "radial_IAE_m_s": 5.96563549782589,
  "signed_longitudinal_delta_m": -0.10215534987389674,
  "tail_speed_mean_m_s": -8.068467080846772e-05,
  "tail_speed_rms_m_s": 0.007690253903648164,
  "tail_sensor_speed_mean_m_s": 0.00018605111010302962,
  "tail_fk_speed_mean_m_s": 2.337674396920386e-05,
  "peak_tilt_rad": 0.18024954221938283,
  "peak_wheel_torque_nm": 2.0284125804901123,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.49395299142714383,
  "final_integral_m_s": -0.5026744794785291,
  "elapsed_wall_s": 8.663076527998783
}
```
