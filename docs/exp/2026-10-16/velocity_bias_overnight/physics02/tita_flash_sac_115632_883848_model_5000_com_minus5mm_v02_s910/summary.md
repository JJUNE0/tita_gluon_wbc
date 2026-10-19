# tita_flash_sac_115632_883848_model_5000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: cc685c5efb437641f8ad47131a1b737aa37ee01ecbc81e3d5e5a21ebc1ddd90d

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_5000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "f0493eceaeb0d984b797dd6231c2ae7ed80e362c6ac6aaaae4a945f80a2fd99a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05159489892684649,
  "max_drift_m": 0.09636584036023663,
  "radial_IAE_m_s": 3.4367527329394907,
  "signed_longitudinal_delta_m": -0.051590038519466294,
  "tail_speed_mean_m_s": 1.6619778284655308e-05,
  "tail_speed_rms_m_s": 0.00011574560692624591,
  "tail_sensor_speed_mean_m_s": 2.412049458942283e-05,
  "tail_fk_speed_mean_m_s": 2.8185111010047744e-05,
  "peak_tilt_rad": 0.18473758514564897,
  "peak_wheel_torque_nm": 3.572049379348755,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4986400910719034,
  "final_integral_m_s": -0.49867151001887217,
  "elapsed_wall_s": 19.062611356028356
}
```
