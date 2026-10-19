# tita_flash_sac_115632_883848_model_10000_com_plus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_com_plus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "50e778000c22d4e4e7cb38ff9fe06351dee1ab90a2ffbe76ef797eeac57a69aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.091689744229462,
  "max_drift_m": 0.09828906097125456,
  "radial_IAE_m_s": 5.398581601354132,
  "signed_longitudinal_delta_m": 0.09168820129213245,
  "tail_speed_mean_m_s": 5.1529775935125994e-05,
  "tail_speed_rms_m_s": 0.022022925683994003,
  "tail_sensor_speed_mean_m_s": 0.00042407924177994313,
  "tail_fk_speed_mean_m_s": 9.09076698292373e-06,
  "peak_tilt_rad": 0.11968599654019774,
  "peak_wheel_torque_nm": 2.9652955532073975,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3628010748040586,
  "final_integral_m_s": 0.3628010748040586,
  "elapsed_wall_s": 11.32159883400891
}
```
