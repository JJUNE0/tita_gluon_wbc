# tita_flash_sac_193248_068255_model_45000_mass1.15_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_mass1.15_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "11bb1b0edb496306b2bcc2f099ec07418b723a8f5e6cd68945e7128a1591c8b8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04039295532136315,
  "max_drift_m": 0.0843752179601148,
  "radial_IAE_m_s": 2.4470521346837346,
  "signed_longitudinal_delta_m": -0.04039206687565345,
  "tail_speed_mean_m_s": 2.639503302023205e-06,
  "tail_speed_rms_m_s": 2.6401326143032982e-06,
  "tail_sensor_speed_mean_m_s": 2.928533386033499e-06,
  "tail_fk_speed_mean_m_s": 5.965216180978644e-07,
  "peak_tilt_rad": 0.13975314603100775,
  "peak_wheel_torque_nm": 1.639553427696228,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.42867988586817196,
  "final_integral_m_s": -0.4286808262424452,
  "elapsed_wall_s": 5.607162566971965
}
```
