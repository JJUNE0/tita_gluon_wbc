# tita_flash_sac_115632_883848_model_5000_mass115_v02_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_mass115_v02_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
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
  "checkpoint_sha256": "cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d",
  "onnx_sha256": "4d80b373930fd59198e3fc588870f929175201ad8b748405f7e94231464a4d30",
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
  "initial_physics_sha256": "be92ee38bae4e94fa8dcbd04ed5cc08854cc5f98d6a85b4623ac840dfe55ad99",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.03663309344686249,
  "max_drift_m": 0.03681523537220207,
  "radial_IAE_m_s": 8.245523081789496,
  "signed_longitudinal_delta_m": -0.036631016526783064,
  "tail_speed_mean_m_s": 0.00014432627664633392,
  "tail_speed_rms_m_s": 0.00671850881095323,
  "tail_sensor_speed_mean_m_s": 0.00014837309650480532,
  "tail_fk_speed_mean_m_s": 0.00013439260442246002,
  "peak_tilt_rad": 0.16520335850489776,
  "peak_wheel_torque_nm": 2.9260172843933105,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.23910534353978208,
  "final_integral_m_s": -0.23992151858742936,
  "elapsed_wall_s": 88.59291966102319
}
```
