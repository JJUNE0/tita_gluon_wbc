# tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "2b59eff138f948c426aa98336a01adaaa5f030e61ce678f789525700cb09c559",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.408287526594978,
  "max_drift_m": 3.408287526594978,
  "radial_IAE_m_s": 101.9259129957126,
  "signed_longitudinal_delta_m": -3.3997008283631334,
  "tail_speed_mean_m_s": -0.056721650442250755,
  "tail_speed_rms_m_s": 0.05672187084146828,
  "tail_sensor_speed_mean_m_s": -0.056599167365665365,
  "tail_fk_speed_mean_m_s": -0.05659922649388885,
  "peak_tilt_rad": 0.02236898726960268,
  "peak_wheel_torque_nm": 0.13281820714473724,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.705704670981504
}
```
