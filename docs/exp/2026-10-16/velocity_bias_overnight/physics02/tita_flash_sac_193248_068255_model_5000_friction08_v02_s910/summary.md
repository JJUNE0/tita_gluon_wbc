# tita_flash_sac_193248_068255_model_5000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
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
  "initial_physics_sha256": "8bb1f8970e6c354f061d2ee353c4ecf57d50b7ff5e91cff71ad4e6f991541528",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09963126558492184,
  "max_drift_m": 0.10148448941177426,
  "radial_IAE_m_s": 5.889933249430344,
  "signed_longitudinal_delta_m": -0.09959519058332265,
  "tail_speed_mean_m_s": 3.0426380925945467e-05,
  "tail_speed_rms_m_s": 3.0871052310224074e-05,
  "tail_sensor_speed_mean_m_s": 2.0957060521021994e-05,
  "tail_fk_speed_mean_m_s": 1.3545260198152214e-05,
  "peak_tilt_rad": 0.07480377643180813,
  "peak_wheel_torque_nm": 1.3637970685958862,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.016265292264082,
  "final_integral_m_s": -1.0162826348149125,
  "elapsed_wall_s": 15.888251823955216
}
```
