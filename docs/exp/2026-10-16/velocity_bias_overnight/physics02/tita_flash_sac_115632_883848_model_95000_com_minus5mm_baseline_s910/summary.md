# tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82",
  "onnx_sha256": "1a45e6567675d4dfc1a738bbe430e52a4f2a2cab73c2c908c46928d22bd54530",
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
  "initial_physics_sha256": "a0d00ff5022ff2b36cfbdfde4de6e005ee2afc5727f74e99a25b753cf361a0a4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.8230010403188076,
  "max_drift_m": 0.8230010403188076,
  "radial_IAE_m_s": 28.687407502303437,
  "signed_longitudinal_delta_m": -0.8225886766945028,
  "tail_speed_mean_m_s": -0.009433225970588686,
  "tail_speed_rms_m_s": 0.009526488914041842,
  "tail_sensor_speed_mean_m_s": -0.009412553209528043,
  "tail_fk_speed_mean_m_s": -0.009412480264086457,
  "peak_tilt_rad": 0.057239533090388095,
  "peak_wheel_torque_nm": 0.1549827754497528,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.45344427600503
}
```
