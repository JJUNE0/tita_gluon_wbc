# tita_flash_sac_115632_883848_model_95000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "46835e166625d2cb62d74cb56c926c223023b5b885c91dff545b5ec8eed7de6c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.006399870775263926,
  "max_drift_m": 0.006399870775263926,
  "radial_IAE_m_s": 0.24619430405977955,
  "signed_longitudinal_delta_m": 0.006393483614368907,
  "tail_speed_mean_m_s": 7.751531485166241e-05,
  "tail_speed_rms_m_s": 7.751768871210725e-05,
  "tail_sensor_speed_mean_m_s": 7.71786672564758e-05,
  "tail_fk_speed_mean_m_s": 7.78231588701201e-05,
  "peak_tilt_rad": 0.062161437806981024,
  "peak_wheel_torque_nm": 0.18992072343826294,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.06283993078857893,
  "final_integral_m_s": 0.06268627483486491,
  "elapsed_wall_s": 14.683932079002261
}
```
