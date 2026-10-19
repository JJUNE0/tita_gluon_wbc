# tita_flash_sac_115632_883848_model_10000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "48422e2724e3c0ac4bfc44896d94d3ed387a67243439ac944822ce49ca34e738",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.09628454166522173,
  "max_drift_m": 0.10941645582199286,
  "radial_IAE_m_s": 26.336767595201387,
  "signed_longitudinal_delta_m": 0.09627877767260508,
  "tail_speed_mean_m_s": -8.097913353857969e-05,
  "tail_speed_rms_m_s": 0.01493306255338374,
  "tail_sensor_speed_mean_m_s": -0.0016527011437281471,
  "tail_fk_speed_mean_m_s": -8.045775259472618e-05,
  "peak_tilt_rad": 0.11421408082891094,
  "peak_wheel_torque_nm": 2.8244266510009766,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30840377720478657,
  "final_integral_m_s": 0.30840377720478657,
  "elapsed_wall_s": 81.25045394501649
}
```
