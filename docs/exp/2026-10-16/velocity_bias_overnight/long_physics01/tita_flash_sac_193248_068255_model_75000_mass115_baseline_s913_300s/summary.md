# tita_flash_sac_193248_068255_model_75000_mass115_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
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
  "initial_physics_sha256": "695374be36fa893cbe4e79c8602cd0cea1b48e37aec0c5cf819f796f71ab3958",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 15.877081315071019,
  "max_drift_m": 16.459466726248948,
  "radial_IAE_m_s": 4210.063020368491,
  "signed_longitudinal_delta_m": -4.854325115197423,
  "tail_speed_mean_m_s": -0.010259053852468362,
  "tail_speed_rms_m_s": 0.01025905411609028,
  "tail_sensor_speed_mean_m_s": -0.010167719072168619,
  "tail_fk_speed_mean_m_s": -0.01012442104529667,
  "peak_tilt_rad": 0.1240004157062029,
  "peak_wheel_torque_nm": 0.5660895109176636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 30.60671912500402
}
```
