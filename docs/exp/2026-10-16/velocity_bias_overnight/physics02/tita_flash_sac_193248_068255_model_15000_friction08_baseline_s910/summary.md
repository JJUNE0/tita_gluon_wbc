# tita_flash_sac_193248_068255_model_15000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_15000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_15000",
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
  "checkpoint_sha256": "04a29ff5621d73fe8056a8ebcd44f66a2477b5d8bc0514955a419f6b336e2081",
  "onnx_sha256": "2c397ad5d7dbe000ce3559aa35152f7b9a9662e19a7069baff210d46a88a6cb4",
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
  "initial_physics_sha256": "c2f3ab32bc7e736d5eaa674b7bccd72d478aa722e950befba59d9e4b4bccce2b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.3796500041944717,
  "max_drift_m": 3.3796500041944717,
  "radial_IAE_m_s": 101.61096191012298,
  "signed_longitudinal_delta_m": -3.3793892059901545,
  "tail_speed_mean_m_s": -0.05605143897258343,
  "tail_speed_rms_m_s": 0.05605159048497291,
  "tail_sensor_speed_mean_m_s": -0.05596270945940492,
  "tail_fk_speed_mean_m_s": -0.055964533375592346,
  "peak_tilt_rad": 0.04461910458045315,
  "peak_wheel_torque_nm": 0.08499482274055481,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.59652521199314
}
```
