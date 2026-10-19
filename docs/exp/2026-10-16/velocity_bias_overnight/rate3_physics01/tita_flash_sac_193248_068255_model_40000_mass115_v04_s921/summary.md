# tita_flash_sac_193248_068255_model_40000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "initial_physics_sha256": "61c3aa046b1298ff8854ccdd1f8428992167b25adda1b88c1d0cd765bc3bd134",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0060878219125161705,
  "max_drift_m": 0.01506430269702635,
  "radial_IAE_m_s": 0.46513900835312694,
  "signed_longitudinal_delta_m": -0.006087753644597494,
  "tail_speed_mean_m_s": 4.8202877672270476e-05,
  "tail_speed_rms_m_s": 4.821350806874283e-05,
  "tail_sensor_speed_mean_m_s": 4.8467784986328207e-05,
  "tail_fk_speed_mean_m_s": 4.7763635128483806e-05,
  "peak_tilt_rad": 0.11468178728408907,
  "peak_wheel_torque_nm": 0.41036278009414673,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.06308242803882921,
  "final_integral_m_s": 0.06308242803882921,
  "elapsed_wall_s": 7.274846153974067
}
```
