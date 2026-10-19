# tita_flash_sac_193248_068255_model_45000_nominal_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "cfc367b42da15abf9f51d7d20cc83e87b54f001e23dd44e02cae134e79b836f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02019352321032123,
  "max_drift_m": 0.035464438377466684,
  "radial_IAE_m_s": 1.2485093704630432,
  "signed_longitudinal_delta_m": -0.02019025989748059,
  "tail_speed_mean_m_s": 1.6795361753455023e-05,
  "tail_speed_rms_m_s": 1.679583433508162e-05,
  "tail_sensor_speed_mean_m_s": 1.769037309314709e-05,
  "tail_fk_speed_mean_m_s": 1.5214501152813808e-05,
  "peak_tilt_rad": 0.07933390643652527,
  "peak_wheel_torque_nm": 0.5798624157905579,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2108984857274101,
  "final_integral_m_s": -0.21092828760349486,
  "elapsed_wall_s": 4.2592403900343925
}
```
