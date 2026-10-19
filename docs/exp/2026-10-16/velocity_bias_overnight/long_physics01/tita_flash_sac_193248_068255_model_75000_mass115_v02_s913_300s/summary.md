# tita_flash_sac_193248_068255_model_75000_mass115_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "final_drift_m": 0.04153040874848654,
  "max_drift_m": 0.07689608592273159,
  "radial_IAE_m_s": 12.572554008645952,
  "signed_longitudinal_delta_m": -0.041522268258018386,
  "tail_speed_mean_m_s": 3.5045664010630183e-06,
  "tail_speed_rms_m_s": 3.5050639619205505e-06,
  "tail_sensor_speed_mean_m_s": 3.4731803149070253e-06,
  "tail_fk_speed_mean_m_s": 3.0728306253320217e-06,
  "peak_tilt_rad": 0.14409635975750446,
  "peak_wheel_torque_nm": 1.5330348014831543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4352965973273816,
  "final_integral_m_s": -0.4353025496326529,
  "elapsed_wall_s": 40.29915265599266
}
```
