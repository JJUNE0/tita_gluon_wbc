# tita_flash_sac_193248_068255_model_100000_com_minus5mm_baseline_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 2b56685ac3bb909b118178fad9d5a6eba842ceb7c9f71dc09f84de7b9d807f9a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_100000_com_minus5mm_baseline_s913_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_100000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
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
  "initial_physics_sha256": "aad082f3513fb2ef0311b60c5d58dba6e4bddd570f0d981d73a192e6761f094b",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 7.929349585509602,
  "max_drift_m": 7.929349585509602,
  "radial_IAE_m_s": 1154.8662579493641,
  "signed_longitudinal_delta_m": 7.915571769878765,
  "tail_speed_mean_m_s": 0.028517349801620448,
  "tail_speed_rms_m_s": 0.028517456749009733,
  "tail_sensor_speed_mean_m_s": 0.028455603939532902,
  "tail_fk_speed_mean_m_s": 0.02845541346147598,
  "peak_tilt_rad": 0.04636642644226607,
  "peak_wheel_torque_nm": 0.6483873724937439,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 23.559441121004056
}
```
