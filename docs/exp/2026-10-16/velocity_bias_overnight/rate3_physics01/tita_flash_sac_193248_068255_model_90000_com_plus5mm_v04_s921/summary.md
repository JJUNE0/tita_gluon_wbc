# tita_flash_sac_193248_068255_model_90000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_90000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "d94ec425dcab69bfb8001711468b6ca37297f4e1aec2e9b20535fd106ee98769",
  "onnx_sha256": "aff309a07b913000eb7916a9b3867232296f7834f48d5391c16e7ec4e09b84d2",
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
  "initial_physics_sha256": "b147b85f181a4707ef4048fe5e23c84329796bdd21813313fcfbf23bc295424b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07531828257453162,
  "max_drift_m": 0.11041324330778611,
  "radial_IAE_m_s": 4.272850589145788,
  "signed_longitudinal_delta_m": 0.07531575479124178,
  "tail_speed_mean_m_s": 9.874937594593058e-05,
  "tail_speed_rms_m_s": 0.0001000359233953916,
  "tail_sensor_speed_mean_m_s": 9.879677727941289e-05,
  "tail_fk_speed_mean_m_s": 0.00010018111966102632,
  "peak_tilt_rad": 0.10673384186477408,
  "peak_wheel_torque_nm": 1.233275294303894,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6944532097001759,
  "final_integral_m_s": 0.6944532097001759,
  "elapsed_wall_s": 8.691378535993863
}
```
