# tita_flash_sac_115632_883848_model_20000_kick-0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick-0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "initial_physics_sha256": "08168cb2cbebf78f9eb6b4cd3fe9dad7c96034064be71c27dc05bec14556a399",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.035068144905177914,
  "max_drift_m": 0.0625766024036439,
  "radial_IAE_m_s": 2.135340991918426,
  "signed_longitudinal_delta_m": -0.03506209572726229,
  "tail_speed_mean_m_s": -1.3737355899849147e-07,
  "tail_speed_rms_m_s": 0.00027543944907682525,
  "tail_sensor_speed_mean_m_s": 5.835662341850706e-06,
  "tail_fk_speed_mean_m_s": 1.5468374825701488e-05,
  "peak_tilt_rad": 0.14624264817138632,
  "peak_wheel_torque_nm": 1.1974163055419922,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26901237534845224,
  "final_integral_m_s": 0.26901237534845224,
  "elapsed_wall_s": 9.186877434025519
}
```
