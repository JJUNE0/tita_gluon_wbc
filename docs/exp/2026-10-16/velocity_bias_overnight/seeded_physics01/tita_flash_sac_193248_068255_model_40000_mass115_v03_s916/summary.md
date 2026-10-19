# tita_flash_sac_193248_068255_model_40000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "56c72ae7aa91dfe9503b7ef82d2f876b5de23e5620a91dcc8fdd36b4c1168479",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006087912551676348,
  "max_drift_m": 0.01506433371500153,
  "radial_IAE_m_s": 0.46514222343453776,
  "signed_longitudinal_delta_m": -0.006087844301107847,
  "tail_speed_mean_m_s": 4.8202771702669916e-05,
  "tail_speed_rms_m_s": 4.821355423491141e-05,
  "tail_sensor_speed_mean_m_s": 4.8467644736731514e-05,
  "tail_fk_speed_mean_m_s": 4.776343452995445e-05,
  "peak_tilt_rad": 0.11468178293578779,
  "peak_wheel_torque_nm": 0.41035646200180054,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.06308232552111014,
  "final_integral_m_s": 0.06308232552111014,
  "elapsed_wall_s": 9.942187489999924
}
```
