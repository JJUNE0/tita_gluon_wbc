# tita_flash_sac_193248_068255_model_75000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "6b2ec49e7940edc5bf31b1df1514327db976e85d0bb544cea4cc1112130ce352",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02994259810342575,
  "max_drift_m": 0.11795958729154428,
  "radial_IAE_m_s": 1.8650516613765782,
  "signed_longitudinal_delta_m": -0.029832492877419063,
  "tail_speed_mean_m_s": -0.00011668891907452064,
  "tail_speed_rms_m_s": 0.008530351484378048,
  "tail_sensor_speed_mean_m_s": -0.0007506721584983657,
  "tail_fk_speed_mean_m_s": -4.020305537679473e-05,
  "peak_tilt_rad": 0.1689748863059939,
  "peak_wheel_torque_nm": 2.2340927124023438,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.31858985125345035,
  "final_integral_m_s": -0.266482762528101,
  "elapsed_wall_s": 4.442897325032391
}
```
