# tita_flash_sac_193248_068255_model_75000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a",
  "onnx_sha256": "ba89df992b5d2cb9fbeaff0a274ee0d50d022a90cd2982cdd88750a3adf35d15",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "45add98c66d87597f0623533321114a1eeda90d086602ed510df897a279cf27b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01836378805730462,
  "max_drift_m": 0.08680739359630331,
  "radial_IAE_m_s": 1.2766627354728546,
  "signed_longitudinal_delta_m": 0.018322987804990278,
  "tail_speed_mean_m_s": -1.9590700980372845e-05,
  "tail_speed_rms_m_s": 0.004442854149723386,
  "tail_sensor_speed_mean_m_s": 0.00012998075530279535,
  "tail_fk_speed_mean_m_s": 9.087490176788329e-06,
  "peak_tilt_rad": 0.19584739622177416,
  "peak_wheel_torque_nm": 2.3511366844177246,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5045344937667545,
  "final_integral_m_s": -0.5045344937667545,
  "elapsed_wall_s": 8.729985736019444
}
```
