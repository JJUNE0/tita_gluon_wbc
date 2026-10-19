# tita_flash_sac_193248_068255_model_100000_b+0.00

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_b+0.00",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
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
  "initial_physics_sha256": "9b23da38aff2165268fad70056674ab4a079b8ea750653868f3f9d362922b0e8",
  "complete": true,
  "failure": [],
  "duration_s": 40.0,
  "final_drift_m": 2.7957808229729255,
  "max_drift_m": 2.7957808229729255,
  "radial_IAE_m_s": 56.24709906803595,
  "signed_longitudinal_delta_m": 2.795666582942647,
  "tail_speed_mean_m_s": 0.0692668706852546,
  "tail_speed_rms_m_s": 0.06926754940186383,
  "tail_sensor_speed_mean_m_s": 0.06911720441719865,
  "tail_fk_speed_mean_m_s": 0.06911766933055476,
  "peak_tilt_rad": 0.05235173263298054,
  "peak_wheel_torque_nm": 0.024873584508895874,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.088779626006726
}
```
