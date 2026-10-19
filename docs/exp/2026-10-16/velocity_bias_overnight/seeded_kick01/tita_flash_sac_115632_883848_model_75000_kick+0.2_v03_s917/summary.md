# tita_flash_sac_115632_883848_model_75000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_75000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_75000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "381e846e3ffb1d5a9ed629c02b55c9740ec3c5b089ca443f38b3d73b6abbd730",
  "onnx_sha256": "2bd3f78d10bc3b7cc4e50272d0289147f13b0a62ac6730048ba653ae53f35114",
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
  "initial_physics_sha256": "72dd3b16ae1ec0e18dab2ec793c22110949f90b73330649a96c7d09c59cf1cc8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04235249209902604,
  "max_drift_m": 0.099082524108793,
  "radial_IAE_m_s": 2.5627208913952546,
  "signed_longitudinal_delta_m": 0.042351031946596576,
  "tail_speed_mean_m_s": 2.4356657098403716e-05,
  "tail_speed_rms_m_s": 2.4616742170497716e-05,
  "tail_sensor_speed_mean_m_s": 2.4359859061136038e-05,
  "tail_fk_speed_mean_m_s": 2.501895498477911e-05,
  "peak_tilt_rad": 0.06948740585643276,
  "peak_wheel_torque_nm": 1.6608023643493652,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004722647961110715,
  "final_integral_m_s": 0.004722647961110715,
  "elapsed_wall_s": 10.541949781996664
}
```
