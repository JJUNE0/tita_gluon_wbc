# tita_flash_sac_193248_068255_model_45000_tau0.1_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_tau0.1_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "ee20a5dfbb46fcd5db6ff635aa3faa46a88abe17e4b58b2b5ba1d4dab1b43af2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02018661786672644,
  "max_drift_m": 0.03752772748120579,
  "radial_IAE_m_s": 1.248727160811549,
  "signed_longitudinal_delta_m": -0.020183452742701554,
  "tail_speed_mean_m_s": 1.67915544921419e-05,
  "tail_speed_rms_m_s": 1.679207978158856e-05,
  "tail_sensor_speed_mean_m_s": 1.7687339634597486e-05,
  "tail_fk_speed_mean_m_s": 1.5210108953796977e-05,
  "peak_tilt_rad": 0.08136115465179516,
  "peak_wheel_torque_nm": 0.49254050850868225,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2108820687485891,
  "final_integral_m_s": -0.21091183115808876,
  "elapsed_wall_s": 7.265180070011411
}
```
