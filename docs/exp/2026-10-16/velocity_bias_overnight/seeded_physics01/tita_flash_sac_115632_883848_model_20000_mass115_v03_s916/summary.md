# tita_flash_sac_115632_883848_model_20000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "5020a7c6ece0629d9a3db904cdde1c3aa8107024d18f040a138926cde9ee5e1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010300422083561167,
  "max_drift_m": 0.05822987389710204,
  "radial_IAE_m_s": 0.7043287638586136,
  "signed_longitudinal_delta_m": -0.010117513306338293,
  "tail_speed_mean_m_s": -0.0010590626836711706,
  "tail_speed_rms_m_s": 0.010580788484612174,
  "tail_sensor_speed_mean_m_s": -0.0011224967596376054,
  "tail_fk_speed_mean_m_s": -0.0010451632841118627,
  "peak_tilt_rad": 0.1772165095067728,
  "peak_wheel_torque_nm": 0.8403133153915405,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19554124845970894,
  "final_integral_m_s": 0.19554124845970894,
  "elapsed_wall_s": 10.439567111956421
}
```
