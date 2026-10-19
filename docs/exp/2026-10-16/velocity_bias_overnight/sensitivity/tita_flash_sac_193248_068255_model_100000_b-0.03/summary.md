# tita_flash_sac_193248_068255_model_100000_b-0.03

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_b-0.03",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.03
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
  "final_drift_m": 3.2687774976652118,
  "max_drift_m": 3.2687774976652118,
  "radial_IAE_m_s": 65.18161801411131,
  "signed_longitudinal_delta_m": 3.2686429273378006,
  "tail_speed_mean_m_s": 0.08183441806645339,
  "tail_speed_rms_m_s": 0.08183479111123419,
  "tail_sensor_speed_mean_m_s": 0.08165758997756534,
  "tail_fk_speed_mean_m_s": 0.08165815133098038,
  "peak_tilt_rad": 0.0542746684502462,
  "peak_wheel_torque_nm": 0.03877246379852295,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.03,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.1433625940117054
}
```
