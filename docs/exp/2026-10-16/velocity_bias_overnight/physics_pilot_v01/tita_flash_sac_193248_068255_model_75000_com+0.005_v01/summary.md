# tita_flash_sac_193248_068255_model_75000_com+0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 3f7331c3912ccec2acc34ba899d124f69c63f6969c89cf609ed1c0b8f22fcd9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_75000_com+0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_75000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "9b1d5cdc3eec3a1331258ec52971444e0e61698f4b947d23040342930bb5ecdd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017549881708420045,
  "max_drift_m": 0.05472791784703001,
  "radial_IAE_m_s": 1.0969783974326457,
  "signed_longitudinal_delta_m": -0.01754954177364788,
  "tail_speed_mean_m_s": 1.5427406863998452e-05,
  "tail_speed_rms_m_s": 1.5462725368431904e-05,
  "tail_sensor_speed_mean_m_s": 1.5609822598144263e-05,
  "tail_fk_speed_mean_m_s": 1.50513960215192e-05,
  "peak_tilt_rad": 0.0919195008685103,
  "peak_wheel_torque_nm": 1.2332465648651123,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19275739361296781,
  "final_integral_m_s": -0.19278502738459152,
  "elapsed_wall_s": 5.432537419022992
}
```
