# tita_flash_sac_193248_068255_model_100000_v03_runtime_s915

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_v03_runtime_s915",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
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
  "initial_physics_sha256": "2ca935a986ee6b07e5c774e6bacefa70c69e2239a0201541f3e28aca821cbf0d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.028238925448953747,
  "max_drift_m": 0.04588513487893073,
  "radial_IAE_m_s": 1.6704511732950897,
  "signed_longitudinal_delta_m": 0.028238416347866335,
  "tail_speed_mean_m_s": 2.4434907860501125e-05,
  "tail_speed_rms_m_s": 2.4435068484337097e-05,
  "tail_sensor_speed_mean_m_s": 2.4340692328554584e-05,
  "tail_fk_speed_mean_m_s": 2.4359399937441188e-05,
  "peak_tilt_rad": 0.05141089090369877,
  "peak_wheel_torque_nm": 0.5504029393196106,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26229303301223744,
  "final_integral_m_s": 0.26229303301223744,
  "elapsed_wall_s": 15.365326679951977
}
```
