# tita_flash_sac_193248_068255_model_85000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "c9262a3b00666f797b9fdf98f6b4145a82ae0a78141d1195f6b7bc81e47ea758",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.017749961322468404,
  "max_drift_m": 0.042295909921053566,
  "radial_IAE_m_s": 3.0245168574997976,
  "signed_longitudinal_delta_m": 0.017741811621130435,
  "tail_speed_mean_m_s": 5.041708786380109e-05,
  "tail_speed_rms_m_s": 5.0678192104151093e-05,
  "tail_sensor_speed_mean_m_s": 5.046529042345571e-05,
  "tail_fk_speed_mean_m_s": 4.984519614816622e-05,
  "peak_tilt_rad": 0.05940355577593781,
  "peak_wheel_torque_nm": 0.582275390625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24868600778007283,
  "final_integral_m_s": 0.24868600778007283,
  "elapsed_wall_s": 26.663331741001457
}
```
