# tita_flash_sac_193248_068255_model_40000_mass130_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass130_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
  "initial_physics_sha256": "2c138b849810644117d57b6abc58a357483830174969ef33f764297361444cf9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0017758252950031343,
  "max_drift_m": 0.020266576663955614,
  "radial_IAE_m_s": 0.07235794595225307,
  "signed_longitudinal_delta_m": 0.0017713032311729663,
  "tail_speed_mean_m_s": 3.9848174502775364e-05,
  "tail_speed_rms_m_s": 3.985293828709567e-05,
  "tail_sensor_speed_mean_m_s": 3.989822331684835e-05,
  "tail_fk_speed_mean_m_s": 3.926151247788041e-05,
  "peak_tilt_rad": 0.15471271854504343,
  "peak_wheel_torque_nm": 0.4386877119541168,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12454519243627782,
  "final_integral_m_s": -0.12454519243627782,
  "elapsed_wall_s": 10.163740943011362
}
```
