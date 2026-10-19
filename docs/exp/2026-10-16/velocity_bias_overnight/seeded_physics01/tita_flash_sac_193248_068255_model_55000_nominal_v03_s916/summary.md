# tita_flash_sac_193248_068255_model_55000_nominal_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_nominal_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "b13f1aa6e92bfda4d36c14a740cdcc539f66a2cf7380c4e21d4d5b5b2f4e7055",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023888998283144114,
  "max_drift_m": 0.07825970475174797,
  "radial_IAE_m_s": 1.8576657770269673,
  "signed_longitudinal_delta_m": -0.023887224333084333,
  "tail_speed_mean_m_s": 0.00021571702602907902,
  "tail_speed_rms_m_s": 0.00021572943695830464,
  "tail_sensor_speed_mean_m_s": 0.00021584050720997277,
  "tail_fk_speed_mean_m_s": 0.00021419263415935365,
  "peak_tilt_rad": 0.13777851422025367,
  "peak_wheel_torque_nm": 0.7942575812339783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30727687688378014,
  "final_integral_m_s": 0.30727687688378014,
  "elapsed_wall_s": 9.86744003999047
}
```
