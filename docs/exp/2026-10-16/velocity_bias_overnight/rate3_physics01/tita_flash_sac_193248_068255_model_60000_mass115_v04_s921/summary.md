# tita_flash_sac_193248_068255_model_60000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "7845c8816af497b7af003c5cf4681e4dd09a0efd8caa13cea6cbaab0a8e2edbf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035219502233840946,
  "max_drift_m": 0.05008094720680389,
  "radial_IAE_m_s": 2.1728116210647586,
  "signed_longitudinal_delta_m": -0.035202883482277014,
  "tail_speed_mean_m_s": 2.765169820457216e-05,
  "tail_speed_rms_m_s": 2.7655719887959918e-05,
  "tail_sensor_speed_mean_m_s": 2.7636553747700215e-05,
  "tail_fk_speed_mean_m_s": 2.7732502356039567e-05,
  "peak_tilt_rad": 0.09811770386512064,
  "peak_wheel_torque_nm": 0.7151824235916138,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3791896623972057,
  "final_integral_m_s": -0.3791896623972057,
  "elapsed_wall_s": 8.429969524033368
}
```
