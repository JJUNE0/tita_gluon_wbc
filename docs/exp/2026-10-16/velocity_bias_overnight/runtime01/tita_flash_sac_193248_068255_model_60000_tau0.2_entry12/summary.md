# tita_flash_sac_193248_068255_model_60000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "e310e30fcbb352321343fbc627528390a485fb77b6b21d6799a7afa74e9df431",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0012097894978765778,
  "max_drift_m": 0.005529588407496862,
  "radial_IAE_m_s": 0.13380048389976495,
  "signed_longitudinal_delta_m": -0.0011408857654175936,
  "tail_speed_mean_m_s": 3.4065775098306725e-05,
  "tail_speed_rms_m_s": 3.406908042708076e-05,
  "tail_sensor_speed_mean_m_s": 3.373512170358172e-05,
  "tail_fk_speed_mean_m_s": 3.5967141789292536e-05,
  "peak_tilt_rad": 0.03971368866108449,
  "peak_wheel_torque_nm": 0.12236537784337997,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.0115569191759742,
  "final_integral_m_s": -0.011627328710111884,
  "elapsed_wall_s": 18.10538489097962
}
```
