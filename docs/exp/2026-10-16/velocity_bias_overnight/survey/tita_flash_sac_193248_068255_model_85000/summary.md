# tita_flash_sac_193248_068255_model_85000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "793199342d603ee2454fd8749f6a3fdc5dc9a420b9789379edb6d97afcb5199e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.057857622314682,
  "max_drift_m": 7.057857622314682,
  "radial_IAE_m_s": 208.8329207134317,
  "signed_longitudinal_delta_m": 7.049196173327575,
  "tail_speed_mean_m_s": 0.12064203198502386,
  "tail_speed_rms_m_s": 0.1206430496263697,
  "tail_sensor_speed_mean_m_s": 0.12038133690576595,
  "tail_fk_speed_mean_m_s": 0.1203792346788763,
  "peak_tilt_rad": 0.06896825780002147,
  "peak_wheel_torque_nm": 0.03170514106750488,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.259199107997119
}
```
