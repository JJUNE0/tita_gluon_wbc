# tita_flash_sac_115632_883848_model_35000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "4b1275497c63ddd46e9a4983b7372d400f8f95b80224a08aa03fe6d693540f60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009797662491549338,
  "max_drift_m": 0.04203665185807742,
  "radial_IAE_m_s": 0.5369956624214771,
  "signed_longitudinal_delta_m": 0.00979582774122263,
  "tail_speed_mean_m_s": 5.261262335119513e-05,
  "tail_speed_rms_m_s": 5.266652354809869e-05,
  "tail_sensor_speed_mean_m_s": 5.26722528524139e-05,
  "tail_fk_speed_mean_m_s": 5.3784768407576574e-05,
  "peak_tilt_rad": 0.13546323720174303,
  "peak_wheel_torque_nm": 1.5939099788665771,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.35191159700576014,
  "final_integral_m_s": 0.35191159700576014,
  "elapsed_wall_s": 11.188131840026472
}
```
