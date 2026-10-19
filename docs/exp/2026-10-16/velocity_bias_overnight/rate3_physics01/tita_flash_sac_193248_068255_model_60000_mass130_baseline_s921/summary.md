# tita_flash_sac_193248_068255_model_60000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "27ba2bc2d19b4b6c8b34414930a6f65f7013673c81330d52016d2a43031b6e97",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.074700186227837,
  "max_drift_m": 11.074700186227837,
  "radial_IAE_m_s": 332.4065122303572,
  "signed_longitudinal_delta_m": -10.987334302260836,
  "tail_speed_mean_m_s": -0.1849775922923787,
  "tail_speed_rms_m_s": 0.1849777403383517,
  "tail_sensor_speed_mean_m_s": -0.18458374418315082,
  "tail_fk_speed_mean_m_s": -0.1845781965918066,
  "peak_tilt_rad": 0.03640603752316407,
  "peak_wheel_torque_nm": 0.6598182320594788,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.449933133961167
}
```
