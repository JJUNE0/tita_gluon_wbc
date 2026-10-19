# tita_flash_sac_193248_068255_model_75000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "35355f1ae0fb649df55a565c83168166638bc9dca2611e89baaa5cf3935508f4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0014661049507232234,
  "max_drift_m": 0.07303203219866862,
  "radial_IAE_m_s": 0.29769096748494794,
  "signed_longitudinal_delta_m": 0.001374329489723104,
  "tail_speed_mean_m_s": 4.859342901614634e-06,
  "tail_speed_rms_m_s": 4.8801794123952744e-06,
  "tail_sensor_speed_mean_m_s": 4.892273781939832e-06,
  "tail_fk_speed_mean_m_s": 4.365432872346642e-06,
  "peak_tilt_rad": 0.14079167502659895,
  "peak_wheel_torque_nm": 1.1745284795761108,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4403424455553116,
  "final_integral_m_s": -0.4403424455553116,
  "elapsed_wall_s": 9.643846595019568
}
```
