# tita_flash_sac_193248_068255_model_5000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "488314b792b700703eecc586439f7f9336cdaf79e68aaebbb937726a19bae7b8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.10329059718911267,
  "max_drift_m": 0.10453506651521302,
  "radial_IAE_m_s": 6.101301869627726,
  "signed_longitudinal_delta_m": -0.10328266128049823,
  "tail_speed_mean_m_s": 1.862546549684789e-05,
  "tail_speed_rms_m_s": 1.8649549900348724e-05,
  "tail_sensor_speed_mean_m_s": 1.3358204985384954e-05,
  "tail_fk_speed_mean_m_s": 8.103715831290092e-06,
  "peak_tilt_rad": 0.0735657759581001,
  "peak_wheel_torque_nm": 0.7412395477294922,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.0483739877286813,
  "final_integral_m_s": -1.0483886441613248,
  "elapsed_wall_s": 13.459764352010097
}
```
