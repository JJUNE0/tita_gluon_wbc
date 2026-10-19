# tita_flash_sac_193248_068255_model_75000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "1581b9d41455b3348716060cfa3f77b88213d2b86f9e557cc372bc3ba827ce7b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.720485848718802,
  "max_drift_m": 14.720485848718802,
  "radial_IAE_m_s": 441.7609690812865,
  "signed_longitudinal_delta_m": -12.041602673014621,
  "tail_speed_mean_m_s": -0.29575211006605046,
  "tail_speed_rms_m_s": 0.2958288782525707,
  "tail_sensor_speed_mean_m_s": -0.2954013994938436,
  "tail_fk_speed_mean_m_s": -0.29543430265193577,
  "peak_tilt_rad": 0.041600588591742316,
  "peak_wheel_torque_nm": 0.2557993531227112,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.31901450798614
}
```
