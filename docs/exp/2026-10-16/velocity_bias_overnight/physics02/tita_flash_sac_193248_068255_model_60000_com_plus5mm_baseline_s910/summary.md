# tita_flash_sac_193248_068255_model_60000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "595d36f087c11ee78f25fa6d2fcd4c25e7464d9eb80cfe9334a08d9318683d41",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.059786910074435,
  "max_drift_m": 1.059786910074435,
  "radial_IAE_m_s": 29.810194229625473,
  "signed_longitudinal_delta_m": 1.0589322906151206,
  "tail_speed_mean_m_s": 0.019780387391692182,
  "tail_speed_rms_m_s": 0.019787574582744095,
  "tail_sensor_speed_mean_m_s": 0.019737299180848544,
  "tail_fk_speed_mean_m_s": 0.019738070047169407,
  "peak_tilt_rad": 0.03960833560526056,
  "peak_wheel_torque_nm": 0.10515737533569336,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.858238507003989
}
```
