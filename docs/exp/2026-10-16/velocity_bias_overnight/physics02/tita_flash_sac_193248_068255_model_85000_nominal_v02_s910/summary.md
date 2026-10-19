# tita_flash_sac_193248_068255_model_85000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "ae995617f5ac22560d3e6f23738b63cf213512da0f03b1ba859111ac68d02fb5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018622246245787736,
  "max_drift_m": 0.03359665130469307,
  "radial_IAE_m_s": 1.0398465350465425,
  "signed_longitudinal_delta_m": 0.018622113868822156,
  "tail_speed_mean_m_s": 3.892980885661979e-05,
  "tail_speed_rms_m_s": 3.897582687892644e-05,
  "tail_sensor_speed_mean_m_s": 3.896787047473435e-05,
  "tail_fk_speed_mean_m_s": 3.8660026295808256e-05,
  "peak_tilt_rad": 0.05960636493307958,
  "peak_wheel_torque_nm": 0.7010430097579956,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19153860867422062,
  "final_integral_m_s": 0.19146821381145254,
  "elapsed_wall_s": 12.148923060041852
}
```
