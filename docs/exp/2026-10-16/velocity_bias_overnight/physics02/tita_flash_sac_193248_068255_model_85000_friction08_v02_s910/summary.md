# tita_flash_sac_193248_068255_model_85000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "9940532335cd91e772e26cd32bd8355dddefd65791e74313c0736dc8b7c7f473",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017525237132845484,
  "max_drift_m": 0.031055136483529675,
  "radial_IAE_m_s": 0.9471036454464392,
  "signed_longitudinal_delta_m": 0.017525033022149365,
  "tail_speed_mean_m_s": 5.989366544144749e-05,
  "tail_speed_rms_m_s": 5.9897175050545625e-05,
  "tail_sensor_speed_mean_m_s": 5.9859752027783434e-05,
  "tail_fk_speed_mean_m_s": 5.9661812499395594e-05,
  "peak_tilt_rad": 0.058234851567938284,
  "peak_wheel_torque_nm": 0.6595649719238281,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18043909115779816,
  "final_integral_m_s": 0.180326371855098,
  "elapsed_wall_s": 17.307689311972354
}
```
