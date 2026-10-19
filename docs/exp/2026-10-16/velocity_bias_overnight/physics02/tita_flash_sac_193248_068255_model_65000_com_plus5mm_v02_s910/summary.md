# tita_flash_sac_193248_068255_model_65000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "e789a74e4803823925a288403ad28bc0c38b70f779ddbce290455253f82103f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005141451437232675,
  "max_drift_m": 0.0094693682702468,
  "radial_IAE_m_s": 0.3599826161103192,
  "signed_longitudinal_delta_m": -0.005136343195403996,
  "tail_speed_mean_m_s": 2.752650379934885e-05,
  "tail_speed_rms_m_s": 2.7601862790599655e-05,
  "tail_sensor_speed_mean_m_s": 2.6866920484457635e-05,
  "tail_fk_speed_mean_m_s": 2.8590829749388558e-05,
  "peak_tilt_rad": 0.03931490490470613,
  "peak_wheel_torque_nm": 0.1207183301448822,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.05194908228404379,
  "final_integral_m_s": -0.051997453344412865,
  "elapsed_wall_s": 15.370696189987939
}
```
