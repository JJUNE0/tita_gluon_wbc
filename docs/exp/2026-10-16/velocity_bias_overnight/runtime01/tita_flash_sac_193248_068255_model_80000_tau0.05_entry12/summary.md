# tita_flash_sac_193248_068255_model_80000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
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
  "initial_physics_sha256": "7d8f4134b4c87943adce10f90aed6d399de3f0d4a786eb795905f2fbeff74b1a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011489581324171527,
  "max_drift_m": 0.011489581324171527,
  "radial_IAE_m_s": 0.452081715628451,
  "signed_longitudinal_delta_m": 0.01147775684806787,
  "tail_speed_mean_m_s": 0.00021418078636268475,
  "tail_speed_rms_m_s": 0.0024691988881754318,
  "tail_sensor_speed_mean_m_s": 6.209787029386838e-05,
  "tail_fk_speed_mean_m_s": 0.00022086954650072928,
  "peak_tilt_rad": 0.049869353359404345,
  "peak_wheel_torque_nm": 2.55165958404541,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14611596072890512,
  "final_integral_m_s": 0.1564053738540263,
  "elapsed_wall_s": 19.24201693199575
}
```
