# tita_flash_sac_193248_068255_model_15000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "1d501f02260a0c1c977c2bc11439c8d572b02135839b048cc5e6ca8e339e800d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.022228956933909468,
  "max_drift_m": 0.03114322362039137,
  "radial_IAE_m_s": 1.3199458944905136,
  "signed_longitudinal_delta_m": -0.0222260778690579,
  "tail_speed_mean_m_s": -5.769069730453618e-06,
  "tail_speed_rms_m_s": 5.822842660224118e-06,
  "tail_sensor_speed_mean_m_s": -5.366750848921084e-06,
  "tail_fk_speed_mean_m_s": -2.9688268448713375e-06,
  "peak_tilt_rad": 0.09976113338724546,
  "peak_wheel_torque_nm": 0.6125377416610718,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.22778370551922963,
  "final_integral_m_s": -0.22777703149579437,
  "elapsed_wall_s": 17.733780762995593
}
```
