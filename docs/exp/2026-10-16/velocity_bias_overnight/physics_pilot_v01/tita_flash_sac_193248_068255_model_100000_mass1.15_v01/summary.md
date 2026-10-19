# tita_flash_sac_193248_068255_model_100000_mass1.15_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass1.15_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "mass": 1.15
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "c104d86dfe462cb22f19f38678522b2d99ed775cef4084cce27eb15e9e1a1e91",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.043636898344060225,
  "max_drift_m": 0.04413772966007303,
  "radial_IAE_m_s": 2.085198004453023,
  "signed_longitudinal_delta_m": -0.043621491414383394,
  "tail_speed_mean_m_s": -0.0002786223697559981,
  "tail_speed_rms_m_s": 0.0051836432081822205,
  "tail_sensor_speed_mean_m_s": 0.0013882332928488754,
  "tail_fk_speed_mean_m_s": -1.3354162327003804e-05,
  "peak_tilt_rad": 0.09218213201532222,
  "peak_wheel_torque_nm": 3.047642230987549,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2773189471311392,
  "final_integral_m_s": -0.26068427686194345,
  "elapsed_wall_s": 5.473586056963541
}
```
