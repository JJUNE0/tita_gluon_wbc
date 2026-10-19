# tita_flash_sac_193248_068255_model_100000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "8b3e164e11cfdfc6234b3e2f160743052a0b9a26ad39947a7026b610883e9346",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026041488720961462,
  "max_drift_m": 0.03619275037596603,
  "radial_IAE_m_s": 1.5501097036446936,
  "signed_longitudinal_delta_m": 0.026040886133245397,
  "tail_speed_mean_m_s": 9.716207162743682e-06,
  "tail_speed_rms_m_s": 9.716381499577229e-06,
  "tail_sensor_speed_mean_m_s": 9.651463599235001e-06,
  "tail_fk_speed_mean_m_s": 9.676580228577023e-06,
  "peak_tilt_rad": 0.0514952391348511,
  "peak_wheel_torque_nm": 0.5750999450683594,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2614031797577817,
  "final_integral_m_s": 0.2613836321057405,
  "elapsed_wall_s": 19.579257806006353
}
```
