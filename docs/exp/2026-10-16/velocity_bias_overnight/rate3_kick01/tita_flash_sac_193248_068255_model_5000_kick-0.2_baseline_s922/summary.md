# tita_flash_sac_193248_068255_model_5000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "e0685fd200f76d5946a18be8993302ebfaa59d1c399d98774995120bee270215",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.4707694611070976,
  "max_drift_m": 1.6453324906906561,
  "radial_IAE_m_s": 71.21487997444679,
  "signed_longitudinal_delta_m": -0.19584414724240112,
  "tail_speed_mean_m_s": -0.0444626175029508,
  "tail_speed_rms_m_s": 0.044475045826605795,
  "tail_sensor_speed_mean_m_s": -0.04506826591502836,
  "tail_fk_speed_mean_m_s": -0.045430707612935564,
  "peak_tilt_rad": 0.08905345338232129,
  "peak_wheel_torque_nm": 4.5585784912109375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 7.555722574004903
}
```
