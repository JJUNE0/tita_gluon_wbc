# tita_flash_sac_193248_068255_model_80000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "807659b35dd4e22f175f7a6b98e7600f5bd35a0a4c2adea744e8dbd355984ab6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013963260756386701,
  "max_drift_m": 0.01739383393918524,
  "radial_IAE_m_s": 0.5044411014067011,
  "signed_longitudinal_delta_m": 0.013957022317941053,
  "tail_speed_mean_m_s": 0.0003493786866475939,
  "tail_speed_rms_m_s": 0.0019855807848252337,
  "tail_sensor_speed_mean_m_s": 0.000806796150145593,
  "tail_fk_speed_mean_m_s": 0.00038793529597272723,
  "peak_tilt_rad": 0.05219872539625481,
  "peak_wheel_torque_nm": 2.123974084854126,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18768964620563755,
  "final_integral_m_s": 0.1876347693660787,
  "elapsed_wall_s": 4.524555054027587
}
```
