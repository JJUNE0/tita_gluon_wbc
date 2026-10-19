# tita_flash_sac_115632_883848_model_95000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 7fc976ceb0b69090d3baf26399d36e566e21da7bf1a3f935bf0a1bc7b29a5d82

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_95000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_95000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "af587fcc1bea9f67522982d808c44968e638414c5ed6337ff480c895dae6f801",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008436568869898233,
  "max_drift_m": 0.008436568869898233,
  "radial_IAE_m_s": 0.3416588964564793,
  "signed_longitudinal_delta_m": 0.008430859335647824,
  "tail_speed_mean_m_s": 9.95650441921441e-05,
  "tail_speed_rms_m_s": 0.00010048171417131767,
  "tail_sensor_speed_mean_m_s": 9.927205894964568e-05,
  "tail_fk_speed_mean_m_s": 9.98719696179637e-05,
  "peak_tilt_rad": 0.06099703576929616,
  "peak_wheel_torque_nm": 0.186374694108963,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08365394723500959,
  "final_integral_m_s": 0.0834324614117817,
  "elapsed_wall_s": 14.6986956820474
}
```
