# tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick+0.2_baseline",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
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
  "initial_physics_sha256": "7e35f90a5034f0b300db24a62630edcf49035b077783a81609e9af8f9649af17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.828953457904246,
  "max_drift_m": 12.828953457904246,
  "radial_IAE_m_s": 374.4197116125191,
  "signed_longitudinal_delta_m": -10.722431908274919,
  "tail_speed_mean_m_s": -0.2608852813115644,
  "tail_speed_rms_m_s": 0.26095165918189245,
  "tail_sensor_speed_mean_m_s": -0.26056273756278125,
  "tail_fk_speed_mean_m_s": -0.2605988132417562,
  "peak_tilt_rad": 0.05253836621516883,
  "peak_wheel_torque_nm": 1.6172081232070923,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.6852364969672635
}
```
