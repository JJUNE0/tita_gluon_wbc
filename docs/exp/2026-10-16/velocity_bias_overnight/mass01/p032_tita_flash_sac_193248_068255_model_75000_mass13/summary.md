# p032_tita_flash_sac_193248_068255_model_75000_mass13

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p032_tita_flash_sac_193248_068255_model_75000_mass13",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 10.0,
      "ki": 20.0,
      "tau": 0.02,
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
  "final_drift_m": 0.17600473889544588,
  "max_drift_m": 0.17638344218757254,
  "radial_IAE_m_s": 8.713961492112432,
  "signed_longitudinal_delta_m": -0.17597321416922312,
  "tail_speed_mean_m_s": -0.0011200963074098833,
  "tail_speed_rms_m_s": 0.03531771320687151,
  "tail_sensor_speed_mean_m_s": -0.002177437533634619,
  "tail_fk_speed_mean_m_s": -0.00016482747954348794,
  "peak_tilt_rad": 0.22007499859988155,
  "peak_wheel_torque_nm": 6.4441070556640625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4746949320636496,
  "final_integral_m_s": -0.5066729327376677,
  "elapsed_wall_s": 5.570437773014419
}
```
