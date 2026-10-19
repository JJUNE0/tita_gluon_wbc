# tita_flash_sac_193248_068255_model_85000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
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
  "initial_physics_sha256": "5255476a237f292677892a5d1c050b1a50f18fb581d0b2b576d07c66f11ce4cf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0089112610536828,
  "max_drift_m": 0.015847366224248257,
  "radial_IAE_m_s": 0.4470101586527882,
  "signed_longitudinal_delta_m": 0.008909767408259734,
  "tail_speed_mean_m_s": 5.107096510124579e-05,
  "tail_speed_rms_m_s": 5.109355529927786e-05,
  "tail_sensor_speed_mean_m_s": 5.108849059309702e-05,
  "tail_fk_speed_mean_m_s": 5.083555571864452e-05,
  "peak_tilt_rad": 0.053697625958798234,
  "peak_wheel_torque_nm": 0.38997888565063477,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.09151982809578756,
  "final_integral_m_s": 0.09142227858518036,
  "elapsed_wall_s": 14.182178980030585
}
```
