# tita_flash_sac_193248_068255_model_75000_mass1.15_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass1.15_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
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
  "initial_physics_sha256": "4231c0c721f1a1b786779a948765f33e83b7df74cdb83ce442eab8ee8919611d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04120288863694273,
  "max_drift_m": 0.10974858848852492,
  "radial_IAE_m_s": 2.4902871285398636,
  "signed_longitudinal_delta_m": -0.0412001984211302,
  "tail_speed_mean_m_s": -2.460792453125879e-07,
  "tail_speed_rms_m_s": 1.7454096256289613e-06,
  "tail_sensor_speed_mean_m_s": -1.4637893044267678e-07,
  "tail_fk_speed_mean_m_s": -6.927333204043103e-07,
  "peak_tilt_rad": 0.18465738544931254,
  "peak_wheel_torque_nm": 2.2162556648254395,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4410075855295742,
  "final_integral_m_s": -0.44101122191439485,
  "elapsed_wall_s": 5.391496950003784
}
```
