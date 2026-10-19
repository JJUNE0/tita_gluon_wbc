# tita_flash_sac_193248_068255_model_40000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "c7a90137e909b74caa2b06ce292fe41eea5de6451b3062ece473b539366d2be1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01209418169844856,
  "max_drift_m": 0.019818870040862625,
  "radial_IAE_m_s": 0.7576753669320435,
  "signed_longitudinal_delta_m": -0.012093798287066115,
  "tail_speed_mean_m_s": 1.6253679821220607e-05,
  "tail_speed_rms_m_s": 1.625572654742943e-05,
  "tail_sensor_speed_mean_m_s": 1.635635841236247e-05,
  "tail_fk_speed_mean_m_s": 1.5717885391202732e-05,
  "peak_tilt_rad": 0.15440936705377628,
  "peak_wheel_torque_nm": 0.567261815071106,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12454095060081175,
  "final_integral_m_s": -0.12457163397556963,
  "elapsed_wall_s": 19.22881756001152
}
```
