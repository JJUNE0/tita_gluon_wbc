# tita_flash_sac_193248_068255_model_5000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "f03fe686e8fe24b0828de8907e66761eea044d581f34f8084ef64e784834eb77",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.3433993204908876,
  "max_drift_m": 1.519717437163228,
  "radial_IAE_m_s": 65.01837595531063,
  "signed_longitudinal_delta_m": 0.10162564286119413,
  "tail_speed_mean_m_s": -0.04357825498227879,
  "tail_speed_rms_m_s": 0.04358823279667606,
  "tail_sensor_speed_mean_m_s": -0.04419030416404408,
  "tail_fk_speed_mean_m_s": -0.04455963472594107,
  "peak_tilt_rad": 0.08956210178016533,
  "peak_wheel_torque_nm": 0.22535505890846252,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.425057852000464
}
```
