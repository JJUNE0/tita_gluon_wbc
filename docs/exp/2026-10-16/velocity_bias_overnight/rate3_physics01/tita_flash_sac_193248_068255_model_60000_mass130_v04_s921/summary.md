# tita_flash_sac_193248_068255_model_60000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "27ba2bc2d19b4b6c8b34414930a6f65f7013673c81330d52016d2a43031b6e97",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030569557912825902,
  "max_drift_m": 0.07444819124170121,
  "radial_IAE_m_s": 1.8636134062303094,
  "signed_longitudinal_delta_m": -0.030518012331560925,
  "tail_speed_mean_m_s": -4.4154769358601104e-07,
  "tail_speed_rms_m_s": 4.4901887657075974e-07,
  "tail_sensor_speed_mean_m_s": -4.1622202975450244e-07,
  "tail_fk_speed_mean_m_s": -3.189789300526551e-07,
  "peak_tilt_rad": 0.17332820065694388,
  "peak_wheel_torque_nm": 1.9581964015960693,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.6000021525458951,
  "final_integral_m_s": -0.6000021525458951,
  "elapsed_wall_s": 7.173942235996947
}
```
