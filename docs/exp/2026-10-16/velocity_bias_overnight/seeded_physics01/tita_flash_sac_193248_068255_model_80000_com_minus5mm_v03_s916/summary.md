# tita_flash_sac_193248_068255_model_80000_com_minus5mm_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_minus5mm_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "efa6d4cd63c98903fe63abca247da1d91ee8425ae40396d84a2fd9ef69ebd2fd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.040310100097202546,
  "max_drift_m": 0.057286409843075946,
  "radial_IAE_m_s": 2.320214802007471,
  "signed_longitudinal_delta_m": 0.040310018202625586,
  "tail_speed_mean_m_s": 4.228759036103507e-05,
  "tail_speed_rms_m_s": 0.002581785529816667,
  "tail_sensor_speed_mean_m_s": 0.000662908450594458,
  "tail_fk_speed_mean_m_s": 0.0001587426450244858,
  "peak_tilt_rad": 0.054314630475731374,
  "peak_wheel_torque_nm": 2.162893295288086,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.00820429446659643,
  "final_integral_m_s": 0.00820429446659643,
  "elapsed_wall_s": 13.29667758702999
}
```
