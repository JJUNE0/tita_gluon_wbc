# tita_flash_sac_193248_068255_model_60000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "initial_physics_sha256": "227eb80d004d4fcdab7011f135ba30b4010055f8df6abc14489c3f25e5c1a0e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0020872505895293695,
  "max_drift_m": 0.0068912426137823475,
  "radial_IAE_m_s": 0.19237190470188892,
  "signed_longitudinal_delta_m": -0.0020456229228261627,
  "tail_speed_mean_m_s": 3.575260139425944e-05,
  "tail_speed_rms_m_s": 3.575533339467093e-05,
  "tail_sensor_speed_mean_m_s": 3.517393616720794e-05,
  "tail_fk_speed_mean_m_s": 3.749857834642144e-05,
  "peak_tilt_rad": 0.040900804787322276,
  "peak_wheel_torque_nm": 0.1592862606048584,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.01939921663910861,
  "final_integral_m_s": -0.01947291782178203,
  "elapsed_wall_s": 17.86264373996528
}
```
