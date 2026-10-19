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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "final_drift_m": 0.0399770748691781,
  "max_drift_m": 0.09750983782145198,
  "radial_IAE_m_s": 2.4218172056081233,
  "signed_longitudinal_delta_m": 0.03997556964163595,
  "tail_speed_mean_m_s": 2.4348996610947896e-05,
  "tail_speed_rms_m_s": 2.4608457760363464e-05,
  "tail_sensor_speed_mean_m_s": 2.4350324911347656e-05,
  "tail_fk_speed_mean_m_s": 2.5011124061151453e-05,
  "peak_tilt_rad": 0.06939383420756995,
  "peak_wheel_torque_nm": 1.6652392148971558,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.004719471318304631,
  "final_integral_m_s": 0.004719471318304631,
  "elapsed_wall_s": 10.120693513017613
}
```
