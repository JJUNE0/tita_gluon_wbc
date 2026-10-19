# tita_flash_sac_193248_068255_model_70000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "7bfe7c1ba5e2cbb78fc30f3cf72eb88e98aeaea93d7a583803230e1e1e2910a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.012944934349519035,
  "max_drift_m": 0.021862478825174853,
  "radial_IAE_m_s": 0.7713283571843161,
  "signed_longitudinal_delta_m": 0.012944522639174743,
  "tail_speed_mean_m_s": 5.176786087450122e-06,
  "tail_speed_rms_m_s": 5.177330593902857e-06,
  "tail_sensor_speed_mean_m_s": 5.1825110536475255e-06,
  "tail_fk_speed_mean_m_s": 4.72976513178271e-06,
  "peak_tilt_rad": 0.08519353274349561,
  "peak_wheel_torque_nm": 0.3000918924808502,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.1341619355114963,
  "final_integral_m_s": 0.13415269091429446,
  "elapsed_wall_s": 16.212842004955746
}
```
