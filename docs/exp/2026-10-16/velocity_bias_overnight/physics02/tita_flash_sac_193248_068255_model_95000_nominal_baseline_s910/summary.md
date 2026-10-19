# tita_flash_sac_193248_068255_model_95000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 8.169019905798217,
  "max_drift_m": 8.169019905798217,
  "radial_IAE_m_s": 224.66546326912032,
  "signed_longitudinal_delta_m": -8.024290427616773,
  "tail_speed_mean_m_s": -0.16356350462229174,
  "tail_speed_rms_m_s": 0.16422498922274384,
  "tail_sensor_speed_mean_m_s": -0.16335424819798608,
  "tail_fk_speed_mean_m_s": -0.1633725185015624,
  "peak_tilt_rad": 0.044890479042721365,
  "peak_wheel_torque_nm": 0.2267880141735077,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.136610771995038
}
```
