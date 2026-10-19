# tita_flash_sac_193248_068255_model_95000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "e2f7b442d03c8ccac7a04acff014a74c0848b4600e9502977e5c2c626af53b64",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022447630341316277,
  "max_drift_m": 0.054488726068210376,
  "radial_IAE_m_s": 1.3475054979333514,
  "signed_longitudinal_delta_m": -0.022441774317334403,
  "tail_speed_mean_m_s": 7.820960011615385e-07,
  "tail_speed_rms_m_s": 7.834908214232025e-07,
  "tail_sensor_speed_mean_m_s": 1.0394525022481214e-06,
  "tail_fk_speed_mean_m_s": 4.11132051872618e-07,
  "peak_tilt_rad": 0.08254288950918598,
  "peak_wheel_torque_nm": 0.5554717183113098,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23711385333825355,
  "final_integral_m_s": -0.23711475558934067,
  "elapsed_wall_s": 15.900311824050732
}
```
