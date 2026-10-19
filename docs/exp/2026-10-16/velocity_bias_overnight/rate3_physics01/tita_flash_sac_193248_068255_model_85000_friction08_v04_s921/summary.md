# tita_flash_sac_193248_068255_model_85000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "2be2918ff7660bd47c26b994abcbbe09509e0862ce74304e879dc4058e168c8a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003946972642439812,
  "max_drift_m": 0.04106248032942099,
  "radial_IAE_m_s": 0.35679120551434784,
  "signed_longitudinal_delta_m": 0.003946874227155363,
  "tail_speed_mean_m_s": 5.475449265338196e-05,
  "tail_speed_rms_m_s": 0.0014718559326227887,
  "tail_sensor_speed_mean_m_s": 4.81133589644894e-05,
  "tail_fk_speed_mean_m_s": 5.457003388856409e-05,
  "peak_tilt_rad": 0.05818462041452577,
  "peak_wheel_torque_nm": 0.5536267161369324,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18209048149775256,
  "final_integral_m_s": 0.18209048149775256,
  "elapsed_wall_s": 7.025390814000275
}
```
