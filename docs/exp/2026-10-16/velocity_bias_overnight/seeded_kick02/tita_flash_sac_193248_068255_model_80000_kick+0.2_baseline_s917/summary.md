# tita_flash_sac_193248_068255_model_80000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "f2e08e523894ecefcff1e6f9171658ba18a00248c09319c897e16f6559632cfb",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.8225010100877514,
  "max_drift_m": 2.8225010100877514,
  "radial_IAE_m_s": 86.71979022078139,
  "signed_longitudinal_delta_m": 2.8203737841367014,
  "tail_speed_mean_m_s": 0.04797099972630105,
  "tail_speed_rms_m_s": 0.04806776949961451,
  "tail_sensor_speed_mean_m_s": 0.047458724371547564,
  "tail_fk_speed_mean_m_s": 0.047893845564924604,
  "peak_tilt_rad": 0.061488827753336306,
  "peak_wheel_torque_nm": 2.2388036251068115,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.45704475598177
}
```
