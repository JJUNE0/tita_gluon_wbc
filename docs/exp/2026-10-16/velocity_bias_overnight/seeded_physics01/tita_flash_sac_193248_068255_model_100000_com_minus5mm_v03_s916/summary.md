# tita_flash_sac_193248_068255_model_100000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "84753bee2fe5045ed19137d014a69f81c14f3788b2d880029633887c95e9efcf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.020638537682779234,
  "max_drift_m": 0.023419667261371784,
  "radial_IAE_m_s": 1.1343684026642527,
  "signed_longitudinal_delta_m": 0.02063846181484709,
  "tail_speed_mean_m_s": 5.9735207778618526e-05,
  "tail_speed_rms_m_s": 5.9735988665501704e-05,
  "tail_sensor_speed_mean_m_s": 5.957641300253677e-05,
  "tail_fk_speed_mean_m_s": 5.958791371489914e-05,
  "peak_tilt_rad": 0.04636641933007857,
  "peak_wheel_torque_nm": 0.6336508393287659,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12679817050974185,
  "final_integral_m_s": 0.12679817050974185,
  "elapsed_wall_s": 10.024652991967741
}
```
