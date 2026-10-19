# tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "02eee71f06bad406f72f5570dfddf16b996bfcb0182fc3302c27655f5328b4b5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.187128313213523,
  "max_drift_m": 7.187128313213523,
  "radial_IAE_m_s": 214.06362700432214,
  "signed_longitudinal_delta_m": 7.1862809409164194,
  "tail_speed_mean_m_s": 0.12072146607312065,
  "tail_speed_rms_m_s": 0.12072148988599618,
  "tail_sensor_speed_mean_m_s": 0.12046054047560707,
  "tail_fk_speed_mean_m_s": 0.12046092585872464,
  "peak_tilt_rad": 0.05722823666702559,
  "peak_wheel_torque_nm": 0.590320885181427,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 18.020976300002076
}
```
