# tita_flash_sac_115632_883848_model_15000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_15000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_15000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "checkpoint_sha256": "966f7a286b3139a7c633828fa375c6eeb4645d5eed73f64ed986c1c72dc72003",
  "onnx_sha256": "1fec00b7bc7eebbc5b6decf23ac6f29b8799c5cf64ff1dee51c1ba762cf013ed",
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
  "initial_physics_sha256": "de5c3d31731dd08d02a152c0340eb4ebb5c161dab691cf7d00893c39c161f246",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030126062072698065,
  "max_drift_m": 0.05235630666259072,
  "radial_IAE_m_s": 1.8855696014383283,
  "signed_longitudinal_delta_m": -0.030070149101757992,
  "tail_speed_mean_m_s": 3.306331772734951e-05,
  "tail_speed_rms_m_s": 3.4861520328350106e-05,
  "tail_sensor_speed_mean_m_s": 3.324173104141276e-05,
  "tail_fk_speed_mean_m_s": 3.3889773735316676e-05,
  "peak_tilt_rad": 0.12342825207303831,
  "peak_wheel_torque_nm": 2.532634735107422,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.367324168672778,
  "final_integral_m_s": -0.367324168672778,
  "elapsed_wall_s": 13.523855843988713
}
```
