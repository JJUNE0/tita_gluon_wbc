# tita_flash_sac_193248_068255_model_75000_nominal_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_nominal_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
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
  "initial_physics_sha256": "aad9ba8281f36990f22ffea1046219464f212446f42e476749db094ea4dec8bb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.856499692168576,
  "max_drift_m": 12.856499692168576,
  "radial_IAE_m_s": 376.60094038660327,
  "signed_longitudinal_delta_m": -11.16411028659863,
  "tail_speed_mean_m_s": -0.2553375709556286,
  "tail_speed_rms_m_s": 0.2554202759195761,
  "tail_sensor_speed_mean_m_s": -0.2550397474654391,
  "tail_fk_speed_mean_m_s": -0.25506666814854256,
  "peak_tilt_rad": 0.048301302148458625,
  "peak_wheel_torque_nm": 0.2910778522491455,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.333249461022206
}
```
