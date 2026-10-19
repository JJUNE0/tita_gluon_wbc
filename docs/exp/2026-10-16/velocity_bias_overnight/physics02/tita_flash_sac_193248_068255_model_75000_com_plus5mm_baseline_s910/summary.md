# tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "d0a1e55654f6f905a86004ad0c543a2da9878252f66835c4b88e279eefcce5e5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.281641986682631,
  "max_drift_m": 10.281641986682631,
  "radial_IAE_m_s": 287.5965775846066,
  "signed_longitudinal_delta_m": -8.971026695479688,
  "tail_speed_mean_m_s": -0.21898905354455483,
  "tail_speed_rms_m_s": 0.2191727426943014,
  "tail_sensor_speed_mean_m_s": -0.21871012041602556,
  "tail_fk_speed_mean_m_s": -0.2187459779056544,
  "peak_tilt_rad": 0.05357922501612977,
  "peak_wheel_torque_nm": 0.2868712544441223,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.585565645014867
}
```
