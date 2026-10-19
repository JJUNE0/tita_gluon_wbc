# tita_flash_sac_115632_883848_model_85000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "ac9f2dec546be415eb36fc255f21a26d0cfe087f05eac629e9d68f9983ef9a67",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09313757404394904,
  "max_drift_m": 0.10506200834976709,
  "radial_IAE_m_s": 5.4356404364105835,
  "signed_longitudinal_delta_m": 0.09313601467082491,
  "tail_speed_mean_m_s": -8.083406277184862e-06,
  "tail_speed_rms_m_s": 1.0621928644137202e-05,
  "tail_sensor_speed_mean_m_s": -8.02955959187561e-06,
  "tail_fk_speed_mean_m_s": -7.74092500457323e-06,
  "peak_tilt_rad": 0.06454611831262369,
  "peak_wheel_torque_nm": 1.8783130645751953,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5824352606781489,
  "final_integral_m_s": 0.5824352606781489,
  "elapsed_wall_s": 8.900584690039977
}
```
