# tita_flash_sac_193248_068255_model_85000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "2b748026661591f537d2df452008b9749de7434882edb1a95037f97e47ee6fd2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09623268122414635,
  "max_drift_m": 0.12322550368763198,
  "radial_IAE_m_s": 6.305958073106478,
  "signed_longitudinal_delta_m": 0.09131309033045297,
  "tail_speed_mean_m_s": -0.0008520392081243627,
  "tail_speed_rms_m_s": 0.009813567126050587,
  "tail_sensor_speed_mean_m_s": 7.451173615758374,
  "tail_fk_speed_mean_m_s": 7.451146145400427,
  "peak_tilt_rad": 0.625548881431377,
  "peak_wheel_torque_nm": 9.71200180053711,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.834833970002364
}
```
