# tita_flash_sac_193248_068255_model_100000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
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
  "initial_physics_sha256": "0ad51cbacc768d86a93998ec3637347f157b23a2efc45ff68523a018ac9c623b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.028045759304543616,
  "max_drift_m": 0.04580481288893039,
  "radial_IAE_m_s": 1.6613457542715333,
  "signed_longitudinal_delta_m": 0.02804519031191505,
  "tail_speed_mean_m_s": 2.4196605600739753e-05,
  "tail_speed_rms_m_s": 2.4197615757542732e-05,
  "tail_sensor_speed_mean_m_s": 2.4096847273070288e-05,
  "tail_fk_speed_mean_m_s": 2.4126839884316692e-05,
  "peak_tilt_rad": 0.0514948563861195,
  "peak_wheel_torque_nm": 0.5429744124412537,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2611680179056453,
  "final_integral_m_s": 0.2611680179056453,
  "elapsed_wall_s": 12.152924581954721
}
```
