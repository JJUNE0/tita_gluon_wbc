# tita_flash_sac_193248_068255_model_70000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "e9b4e87cf105d8611032b3b5d1b15f42a36f1d721dc21b3ca252ac882fbf066e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014859470466441541,
  "max_drift_m": 0.02516150638187917,
  "radial_IAE_m_s": 0.8410268469848698,
  "signed_longitudinal_delta_m": 0.014859013662205782,
  "tail_speed_mean_m_s": 3.0005944631591415e-05,
  "tail_speed_rms_m_s": 3.0041937465377962e-05,
  "tail_sensor_speed_mean_m_s": 3.0066155495331407e-05,
  "tail_fk_speed_mean_m_s": 2.9843725062473066e-05,
  "peak_tilt_rad": 0.07963840405588041,
  "peak_wheel_torque_nm": 0.29674211144447327,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.15410755997263956,
  "final_integral_m_s": 0.15405423083707012,
  "elapsed_wall_s": 19.61699490097817
}
```
