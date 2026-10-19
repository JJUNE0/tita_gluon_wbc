# tita_flash_sac_193248_068255_model_60000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 4.919065639805437,
  "max_drift_m": 4.919065639805437,
  "radial_IAE_m_s": 148.38462496144038,
  "signed_longitudinal_delta_m": -4.9033261326771305,
  "tail_speed_mean_m_s": -0.08120290942341875,
  "tail_speed_rms_m_s": 0.08120345697791946,
  "tail_sensor_speed_mean_m_s": -0.08102682917780515,
  "tail_fk_speed_mean_m_s": -0.08102388033097134,
  "peak_tilt_rad": 0.0361967902347049,
  "peak_wheel_torque_nm": 0.10844284296035767,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.593644026957918
}
```
