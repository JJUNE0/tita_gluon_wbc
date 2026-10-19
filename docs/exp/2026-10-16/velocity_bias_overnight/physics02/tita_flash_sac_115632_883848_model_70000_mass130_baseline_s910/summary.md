# tita_flash_sac_115632_883848_model_70000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "0a9c7c48ced8e1b2a0cf5ba991a47a3f4e4617255a56e2927f2fc269721a6093",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.783778810432116,
  "max_drift_m": 9.783778810432116,
  "radial_IAE_m_s": 293.9474762693335,
  "signed_longitudinal_delta_m": -9.78262748460671,
  "tail_speed_mean_m_s": -0.16248023250694366,
  "tail_speed_rms_m_s": 0.16248039890222588,
  "tail_sensor_speed_mean_m_s": -0.16213130506211515,
  "tail_fk_speed_mean_m_s": -0.16213093835729747,
  "peak_tilt_rad": 0.022684162050105587,
  "peak_wheel_torque_nm": 0.274996280670166,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.965316204994451
}
```
