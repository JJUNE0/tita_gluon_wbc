# tita_flash_sac_115632_883848_model_20000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 915,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0",
    "controller_source_sha256": "6056e5bd50e0d84e7e554e390f2ede0726c82adf059af80911969c1286a3cded"
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
  "initial_physics_sha256": "61f26cc09949118ab397fdbb3616a8fc521f6ec7a94333bcd0ee7f886a0dc3b5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03151041515920622,
  "max_drift_m": 0.0999443510740275,
  "radial_IAE_m_s": 2.044455249839117,
  "signed_longitudinal_delta_m": -0.0314830906549457,
  "tail_speed_mean_m_s": -5.4063737914501375e-05,
  "tail_speed_rms_m_s": 0.0012557555392593816,
  "tail_sensor_speed_mean_m_s": -5.291233746655338e-05,
  "tail_fk_speed_mean_m_s": -4.3304578141294276e-05,
  "peak_tilt_rad": 0.15330263700296753,
  "peak_wheel_torque_nm": 0.8841932415962219,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2700675220043488,
  "final_integral_m_s": 0.2700675220043488,
  "elapsed_wall_s": 18.608103103993926
}
```
