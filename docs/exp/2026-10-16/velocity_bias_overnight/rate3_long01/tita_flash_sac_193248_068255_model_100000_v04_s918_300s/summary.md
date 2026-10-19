# tita_flash_sac_193248_068255_model_100000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "initial_physics_sha256": "3fedc11efdd40237efce752ca6e86656605aaef779bc0706c06652d5cae1d218",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.03424690442207219,
  "max_drift_m": 0.04574901152727662,
  "radial_IAE_m_s": 9.065896181508123,
  "signed_longitudinal_delta_m": 0.034246889398840935,
  "tail_speed_mean_m_s": 1.4396454044617485e-05,
  "tail_speed_rms_m_s": 1.7466335810300833e-05,
  "tail_sensor_speed_mean_m_s": 1.4368352919110248e-05,
  "tail_fk_speed_mean_m_s": 1.4337192159918201e-05,
  "peak_tilt_rad": 0.05154101713822401,
  "peak_wheel_torque_nm": 0.5404351353645325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.28649496215394304,
  "final_integral_m_s": 0.28649496215394304,
  "elapsed_wall_s": 26.364689475973137
}
```
