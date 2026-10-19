# tita_flash_sac_193248_068255_model_80000_friction08_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction08_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.8
    },
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
  "initial_physics_sha256": "e9cc2a377bf64f58ce2a15e1933f8305afd01def9067d73db881b90cfbfd2bb9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.225475736023516,
  "max_drift_m": 2.225475736023516,
  "radial_IAE_m_s": 60.03441504613858,
  "signed_longitudinal_delta_m": 2.2218764064048133,
  "tail_speed_mean_m_s": 0.04359863885965973,
  "tail_speed_rms_m_s": 0.043711519243644165,
  "tail_sensor_speed_mean_m_s": 0.0436035398780093,
  "tail_fk_speed_mean_m_s": 0.04370972256200036,
  "peak_tilt_rad": 0.05378141450831997,
  "peak_wheel_torque_nm": 2.205986976623535,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.790582858026028
}
```
