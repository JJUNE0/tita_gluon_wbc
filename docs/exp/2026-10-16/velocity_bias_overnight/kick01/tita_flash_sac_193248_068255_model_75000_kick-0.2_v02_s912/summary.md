# tita_flash_sac_193248_068255_model_75000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "17f9956a4a6373f65b4c6e719c999351fbec27284b0abbbdecacd94cbc40feaa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.027996195978712855,
  "max_drift_m": 0.14212748650979193,
  "radial_IAE_m_s": 1.8391181732705744,
  "signed_longitudinal_delta_m": -0.02799476906857511,
  "tail_speed_mean_m_s": 1.1562103090529306e-05,
  "tail_speed_rms_m_s": 1.156274648480326e-05,
  "tail_sensor_speed_mean_m_s": 1.1667203956872359e-05,
  "tail_fk_speed_mean_m_s": 1.1251797865191422e-05,
  "peak_tilt_rad": 0.18033420976209236,
  "peak_wheel_torque_nm": 2.421450138092041,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.27637246411295263,
  "final_integral_m_s": -0.27639458160009606,
  "elapsed_wall_s": 12.083427071978804
}
```
