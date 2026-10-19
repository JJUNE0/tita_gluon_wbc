# tita_flash_sac_193248_068255_model_100000_mass115_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass115_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "b3c93dc6e177b4dd5351c14bdfe68e80cca979a0d6477628a6d49b5c2290c0d8",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.1005694469550845,
  "max_drift_m": 0.10092530000695764,
  "radial_IAE_m_s": 19.097736641467918,
  "signed_longitudinal_delta_m": -0.0981545708627452,
  "tail_speed_mean_m_s": -0.000268654550458041,
  "tail_speed_rms_m_s": 0.00469850338376171,
  "tail_sensor_speed_mean_m_s": -0.000560620263600804,
  "tail_fk_speed_mean_m_s": 2.8160347188085784e-05,
  "peak_tilt_rad": 0.0892179870765748,
  "peak_wheel_torque_nm": 2.747789144515991,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2863479305899686,
  "final_integral_m_s": -0.2739876765314699,
  "elapsed_wall_s": 30.97328557795845
}
```
