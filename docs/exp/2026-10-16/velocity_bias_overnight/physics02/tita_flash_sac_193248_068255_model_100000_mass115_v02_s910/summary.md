# tita_flash_sac_193248_068255_model_100000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
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
  "initial_physics_sha256": "18ea42bd541312db844ebcdbff9461c9eeeb23f02076d4751af0f7aa193f9461",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04087223865792393,
  "max_drift_m": 0.04146859049040684,
  "radial_IAE_m_s": 1.9982436242537518,
  "signed_longitudinal_delta_m": -0.04086830394818134,
  "tail_speed_mean_m_s": -0.0002486551660510074,
  "tail_speed_rms_m_s": 0.004912224563297204,
  "tail_sensor_speed_mean_m_s": 0.0002910673477412385,
  "tail_fk_speed_mean_m_s": -1.4727422376489937e-05,
  "peak_tilt_rad": 0.08924425684747717,
  "peak_wheel_torque_nm": 2.74516224861145,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.29686492317265983,
  "final_integral_m_s": -0.27298454153660623,
  "elapsed_wall_s": 25.031950943986885
}
```
