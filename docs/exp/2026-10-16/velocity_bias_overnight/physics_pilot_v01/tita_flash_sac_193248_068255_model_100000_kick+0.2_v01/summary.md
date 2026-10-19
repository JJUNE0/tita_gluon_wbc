# tita_flash_sac_193248_068255_model_100000_kick+0.2_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_kick+0.2_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {},
    "kick": 0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
  },
  "checkpoint_sha256": "2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a",
  "onnx_sha256": "fcd7b62b26d94ec01f945f05940b24a521d0ed55477b8dfa4b0e93c3af756a6c",
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
  "initial_physics_sha256": "06e527cb12e931d3fdbe3c946bcff7f64ffd581b53e30a1e593dae04e40712c8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02667432094121519,
  "max_drift_m": 0.10838240452718109,
  "radial_IAE_m_s": 1.6296725004754036,
  "signed_longitudinal_delta_m": 0.026674192630136255,
  "tail_speed_mean_m_s": 9.82949961550201e-06,
  "tail_speed_rms_m_s": 9.829578032629396e-06,
  "tail_sensor_speed_mean_m_s": 9.767203252650514e-06,
  "tail_fk_speed_mean_m_s": 9.782048839276987e-06,
  "peak_tilt_rad": 0.11187754679060524,
  "peak_wheel_torque_nm": 1.6928818225860596,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26310753248390667,
  "final_integral_m_s": 0.2630879282741573,
  "elapsed_wall_s": 4.2651655889931135
}
```
