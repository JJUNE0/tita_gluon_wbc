# tita_flash_sac_193248_068255_model_45000_com_plus5mm_baseline_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com_plus5mm_baseline_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "7c60ec441af01a3117aa5e225b610242e1a0e96cf37b69f790e62f76e154cfba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.794247356995748,
  "max_drift_m": 5.794247356995748,
  "radial_IAE_m_s": 170.6115674214809,
  "signed_longitudinal_delta_m": -5.7922978135996495,
  "tail_speed_mean_m_s": -0.09920180240735572,
  "tail_speed_rms_m_s": 0.0992032875296208,
  "tail_sensor_speed_mean_m_s": -0.09903935523814401,
  "tail_fk_speed_mean_m_s": -0.09904247541476136,
  "peak_tilt_rad": 0.045875154010025065,
  "peak_wheel_torque_nm": 0.1865919679403305,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.922865664004348
}
```
