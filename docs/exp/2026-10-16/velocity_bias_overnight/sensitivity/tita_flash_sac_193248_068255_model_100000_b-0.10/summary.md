# tita_flash_sac_193248_068255_model_100000_b-0.10

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_b-0.10",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 40.0,
    "seed": 270,
    "warmup": 8.0,
    "law": {
      "mode": "constant",
      "bias": -0.1
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
  "final_drift_m": 4.184014881291668,
  "max_drift_m": 4.184014881291668,
  "radial_IAE_m_s": 82.60161252612197,
  "signed_longitudinal_delta_m": 4.182642150714464,
  "tail_speed_mean_m_s": 0.10588136990889437,
  "tail_speed_rms_m_s": 0.10588172107161738,
  "tail_sensor_speed_mean_m_s": 0.10565255265651721,
  "tail_fk_speed_mean_m_s": 0.10565337435919735,
  "peak_tilt_rad": 0.058516528979966065,
  "peak_wheel_torque_nm": 0.06724593043327332,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 3.1780099300085567
}
```
