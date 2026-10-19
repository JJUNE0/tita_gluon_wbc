# tita_flash_sac_193248_068255_model_90000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "df5fcf127cae1dac715f947840249db93cf5da78ce7c4e8360786adb1d75ce39",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06333009150997782,
  "max_drift_m": 0.07491982546078821,
  "radial_IAE_m_s": 3.663693746773845,
  "signed_longitudinal_delta_m": 0.06332800322174949,
  "tail_speed_mean_m_s": 6.471084695946309e-05,
  "tail_speed_rms_m_s": 6.512120171984874e-05,
  "tail_sensor_speed_mean_m_s": 6.485072287844782e-05,
  "tail_fk_speed_mean_m_s": 6.621946511380989e-05,
  "peak_tilt_rad": 0.10182184744989575,
  "peak_wheel_torque_nm": 1.918043613433838,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6371222427158464,
  "final_integral_m_s": 0.6370114230024125,
  "elapsed_wall_s": 14.365959369984921
}
```
