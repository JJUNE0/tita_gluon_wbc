# tita_flash_sac_193248_068255_model_100000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "66bd2e633e685bb0c47a24743ba4394fe516fe12c0fadd9ebf829b3ba66910df",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013292192963481178,
  "max_drift_m": 0.01600966602319316,
  "radial_IAE_m_s": 0.7551802027834589,
  "signed_longitudinal_delta_m": 0.013292112225767724,
  "tail_speed_mean_m_s": 2.4391966552039727e-05,
  "tail_speed_rms_m_s": 2.4408115419348945e-05,
  "tail_sensor_speed_mean_m_s": 2.4303162651760036e-05,
  "tail_fk_speed_mean_m_s": 2.4315196248074523e-05,
  "peak_tilt_rad": 0.046250785673659145,
  "peak_wheel_torque_nm": 0.6426839828491211,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12978366230958374,
  "final_integral_m_s": 0.12973271982591444,
  "elapsed_wall_s": 22.3691262609791
}
```
