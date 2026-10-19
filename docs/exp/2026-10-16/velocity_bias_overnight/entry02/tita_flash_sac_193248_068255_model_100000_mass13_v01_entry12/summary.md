# tita_flash_sac_193248_068255_model_100000_mass13_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass13_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
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
  "initial_physics_sha256": "eadd8ad3a2da92f1e2c25fe82339740cbc62d0f83febd032a45bead1213fea95",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.07908706374789987,
  "max_drift_m": 0.08179290121361893,
  "radial_IAE_m_s": 3.4390949714387737,
  "signed_longitudinal_delta_m": -0.07908187616530052,
  "tail_speed_mean_m_s": -0.0007749272903545885,
  "tail_speed_rms_m_s": 0.01765495603799504,
  "tail_sensor_speed_mean_m_s": 0.0009699783786168025,
  "tail_fk_speed_mean_m_s": 0.00011802077213922308,
  "peak_tilt_rad": 0.1494922706636972,
  "peak_wheel_torque_nm": 5.125388145446777,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.36528568075179724,
  "final_integral_m_s": -0.35477266058874884,
  "elapsed_wall_s": 6.436018552980386
}
```
