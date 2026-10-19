# tita_flash_sac_193248_068255_model_100000_b+0.10

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_b+0.10",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": 0.1
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
  "final_drift_m": 1.7924025814901787,
  "max_drift_m": 1.7924025814901787,
  "radial_IAE_m_s": 36.64732025319913,
  "signed_longitudinal_delta_m": 1.7923768728792349,
  "tail_speed_mean_m_s": 0.043801254843916566,
  "tail_speed_rms_m_s": 0.04380139775041554,
  "tail_sensor_speed_mean_m_s": 0.043706663091994925,
  "tail_fk_speed_mean_m_s": 0.043706847560864875,
  "peak_tilt_rad": 0.05235173263298054,
  "peak_wheel_torque_nm": 0.03364625573158264,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 2.962244206981268
}
```
