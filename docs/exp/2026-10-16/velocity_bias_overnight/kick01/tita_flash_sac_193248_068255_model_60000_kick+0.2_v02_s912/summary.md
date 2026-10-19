# tita_flash_sac_193248_068255_model_60000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "c31150ef304f0702b56cc4dddbcda3657909e9268ba1160b8190b6041984e74f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0002999934862973,
  "max_drift_m": 0.06459672684087227,
  "radial_IAE_m_s": 0.11642580870940772,
  "signed_longitudinal_delta_m": 0.00028406613453723945,
  "tail_speed_mean_m_s": 3.374680487186937e-05,
  "tail_speed_rms_m_s": 3.375025214893355e-05,
  "tail_sensor_speed_mean_m_s": 3.3452523080543524e-05,
  "tail_fk_speed_mean_m_s": 3.567048920752511e-05,
  "peak_tilt_rad": 0.06891632725945085,
  "peak_wheel_torque_nm": 1.6391005516052246,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.010149601577639288,
  "final_integral_m_s": -0.010219333564641546,
  "elapsed_wall_s": 15.234131461998913
}
```
