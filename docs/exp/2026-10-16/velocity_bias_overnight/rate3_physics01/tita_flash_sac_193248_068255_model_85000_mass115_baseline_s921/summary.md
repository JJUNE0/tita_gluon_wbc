# tita_flash_sac_193248_068255_model_85000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "03eebffd86ad7f57c8c5be66858c8fbcedd4200ce73f2338425f117a2b027691",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.022962348331676,
  "max_drift_m": 6.022962348331676,
  "radial_IAE_m_s": 174.77605067449701,
  "signed_longitudinal_delta_m": -6.011205653712502,
  "tail_speed_mean_m_s": -0.10621201617341584,
  "tail_speed_rms_m_s": 0.10622492966547914,
  "tail_sensor_speed_mean_m_s": -0.10605140730146113,
  "tail_fk_speed_mean_m_s": -0.10605538485217576,
  "peak_tilt_rad": 0.07619314376037556,
  "peak_wheel_torque_nm": 0.9059069752693176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.808005961007439
}
```
