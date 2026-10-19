# tita_flash_sac_193248_068255_model_30000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "a31b0b69ca60fccd3d4e267cf6ea8789af0d546294e71b2154abce7d30072e7a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.133106999323441,
  "max_drift_m": 4.133106999323441,
  "radial_IAE_m_s": 124.59759157701066,
  "signed_longitudinal_delta_m": 4.133017624919997,
  "tail_speed_mean_m_s": 0.06815741592554708,
  "tail_speed_rms_m_s": 0.0681576715538339,
  "tail_sensor_speed_mean_m_s": 0.06801314139494048,
  "tail_fk_speed_mean_m_s": 0.06801093091702803,
  "peak_tilt_rad": 0.027411245639818116,
  "peak_wheel_torque_nm": 0.20368742942810059,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.120867686986458
}
```
