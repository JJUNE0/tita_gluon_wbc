# tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "2830577c8f6653f3b658c73f6bafc708105060f629126d28416261e949a786c9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.9909477403063713,
  "max_drift_m": 1.9909477403063713,
  "radial_IAE_m_s": 71.333389521731,
  "signed_longitudinal_delta_m": -0.6754164956800305,
  "tail_speed_mean_m_s": -0.044506396731772105,
  "tail_speed_rms_m_s": 0.044506613757995854,
  "tail_sensor_speed_mean_m_s": -0.04486882526534896,
  "tail_fk_speed_mean_m_s": -0.04510719779247597,
  "peak_tilt_rad": 0.07719274688931521,
  "peak_wheel_torque_nm": 0.6824477910995483,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.739847166987602
}
```
