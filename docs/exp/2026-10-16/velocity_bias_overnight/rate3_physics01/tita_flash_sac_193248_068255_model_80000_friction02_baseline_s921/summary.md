# tita_flash_sac_193248_068255_model_80000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "initial_physics_sha256": "cf5453aaf34c2b421a644af1c21e8028df4f7d3fd4b323f6e2a05b0a79078f0a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.567113898934745,
  "max_drift_m": 2.567113898934745,
  "radial_IAE_m_s": 70.64503738874186,
  "signed_longitudinal_delta_m": 2.542911861392539,
  "tail_speed_mean_m_s": 0.049228293059847494,
  "tail_speed_rms_m_s": 0.049323628163814,
  "tail_sensor_speed_mean_m_s": 0.04983942972184776,
  "tail_fk_speed_mean_m_s": 0.04927297446690985,
  "peak_tilt_rad": 0.054270661269897325,
  "peak_wheel_torque_nm": 1.805330514907837,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.683151489007287
}
```
