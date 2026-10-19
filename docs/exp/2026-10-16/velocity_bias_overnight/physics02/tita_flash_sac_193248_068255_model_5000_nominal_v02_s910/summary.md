# tita_flash_sac_193248_068255_model_5000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "bd1876362faf0d495c5c521d9ce5e87b3d67338fb7805486d7dc3ee484f8f6dc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09978539214903133,
  "max_drift_m": 0.10093540976684873,
  "radial_IAE_m_s": 5.880579926452517,
  "signed_longitudinal_delta_m": -0.09976217968697577,
  "tail_speed_mean_m_s": 2.1260327483970958e-05,
  "tail_speed_rms_m_s": 2.1266114797017903e-05,
  "tail_sensor_speed_mean_m_s": 1.6674341719346074e-05,
  "tail_fk_speed_mean_m_s": 1.1069862927752683e-05,
  "peak_tilt_rad": 0.07520633115234232,
  "peak_wheel_torque_nm": 0.9384011030197144,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0128917208753712,
  "final_integral_m_s": -1.012914477727951,
  "elapsed_wall_s": 10.64602654799819
}
```
