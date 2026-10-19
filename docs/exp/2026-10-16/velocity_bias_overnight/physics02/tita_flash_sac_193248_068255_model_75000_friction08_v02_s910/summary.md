# tita_flash_sac_193248_068255_model_75000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "c66e3a96bbb1148b4de54d6fe917757ee088adc354242e632857ad84d25bdf3a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027774822940780153,
  "max_drift_m": 0.04963133952886348,
  "radial_IAE_m_s": 1.695894699606603,
  "signed_longitudinal_delta_m": -0.02777273432238855,
  "tail_speed_mean_m_s": 1.5463086151425692e-05,
  "tail_speed_rms_m_s": 1.54639140502214e-05,
  "tail_sensor_speed_mean_m_s": 1.5719996745534332e-05,
  "tail_fk_speed_mean_m_s": 1.5214552662626328e-05,
  "peak_tilt_rad": 0.0871254184762591,
  "peak_wheel_torque_nm": 0.4806603789329529,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2889504281749776,
  "final_integral_m_s": -0.28898033317873306,
  "elapsed_wall_s": 15.875847528979648
}
```
