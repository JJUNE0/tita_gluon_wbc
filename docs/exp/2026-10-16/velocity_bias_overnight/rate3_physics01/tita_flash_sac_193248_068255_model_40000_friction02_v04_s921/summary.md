# tita_flash_sac_193248_068255_model_40000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "fcf1c0a87d9b35a04380446b38a28b9e854cbdae1217973a20e91046f60099cf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024986512294465153,
  "max_drift_m": 0.05418217470636176,
  "radial_IAE_m_s": 1.5348449671266768,
  "signed_longitudinal_delta_m": -0.0249183388918431,
  "tail_speed_mean_m_s": 5.0160746033439526e-06,
  "tail_speed_rms_m_s": 5.510874850986894e-06,
  "tail_sensor_speed_mean_m_s": 4.749224273862109e-06,
  "tail_fk_speed_mean_m_s": 4.238668752446815e-06,
  "peak_tilt_rad": 0.11513584543356425,
  "peak_wheel_torque_nm": 1.04045832157135,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29779971324240745,
  "final_integral_m_s": 0.29779971324240745,
  "elapsed_wall_s": 9.761774807993788
}
```
