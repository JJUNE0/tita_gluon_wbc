# tita_flash_sac_193248_068255_model_60000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
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
  "initial_physics_sha256": "a26cbd07eb770065667311da55b4c3ab0d2ea25a0bbbab971042987aedca5fb6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005393502336514811,
  "max_drift_m": 0.006320555859642222,
  "radial_IAE_m_s": 0.31071802459415343,
  "signed_longitudinal_delta_m": -0.005375478477712136,
  "tail_speed_mean_m_s": -1.2002634735812435e-05,
  "tail_speed_rms_m_s": 0.006284327386362008,
  "tail_sensor_speed_mean_m_s": -3.172983025569541e-06,
  "tail_fk_speed_mean_m_s": 4.7327070657353235e-05,
  "peak_tilt_rad": 0.0527317006192809,
  "peak_wheel_torque_nm": 1.2931967973709106,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23375338039786345,
  "final_integral_m_s": -0.06844694765772774,
  "elapsed_wall_s": 4.42781055305386
}
```
