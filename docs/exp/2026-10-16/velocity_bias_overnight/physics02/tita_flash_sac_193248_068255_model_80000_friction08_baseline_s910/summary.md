# tita_flash_sac_193248_068255_model_80000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "c7f00ec40e77ba15f15396f744042a8053fd4f8b96053a4aac521f56241968b6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.240713062199747,
  "max_drift_m": 2.240713062199747,
  "radial_IAE_m_s": 60.50147438967128,
  "signed_longitudinal_delta_m": 2.237194563294096,
  "tail_speed_mean_m_s": 0.043828197933532695,
  "tail_speed_rms_m_s": 0.043940230791537326,
  "tail_sensor_speed_mean_m_s": 0.043567063423594676,
  "tail_fk_speed_mean_m_s": 0.04393056401323029,
  "peak_tilt_rad": 0.05380782484612423,
  "peak_wheel_torque_nm": 2.206517457962036,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.37158737500431
}
```
