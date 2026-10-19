# tita_flash_sac_193248_068255_model_30000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
    "estimator": "raw"
  },
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "8115e25cb8908cc43966e591043d2cacaa4756fdcf9cf657602b4f4f3c9a7a8a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0018635206071227809,
  "max_drift_m": 0.022707267617947717,
  "radial_IAE_m_s": 0.4887558485269843,
  "signed_longitudinal_delta_m": -0.0016302957615996917,
  "tail_speed_mean_m_s": -0.0004088024098657765,
  "tail_speed_rms_m_s": 0.04425544538193561,
  "tail_sensor_speed_mean_m_s": -0.0005715671379003073,
  "tail_fk_speed_mean_m_s": -0.00021513163706627218,
  "peak_tilt_rad": 0.06250198462560741,
  "peak_wheel_torque_nm": 1.6481164693832397,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2523733845787119,
  "final_integral_m_s": 0.2945193836509072,
  "elapsed_wall_s": 4.384318451979198
}
```
