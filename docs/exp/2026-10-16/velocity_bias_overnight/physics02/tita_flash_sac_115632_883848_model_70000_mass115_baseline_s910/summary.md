# tita_flash_sac_115632_883848_model_70000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "5fc1927ae4a3888df0ba86f9d05ac66da3347ab162707189b5c1303356e2998f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.297346605167698,
  "max_drift_m": 8.297346605167698,
  "radial_IAE_m_s": 248.5163565297038,
  "signed_longitudinal_delta_m": -8.287375375198492,
  "tail_speed_mean_m_s": -0.1384696129497853,
  "tail_speed_rms_m_s": 0.13846965003287057,
  "tail_sensor_speed_mean_m_s": -0.13817104864470425,
  "tail_fk_speed_mean_m_s": -0.1381711178337276,
  "peak_tilt_rad": 0.01651519119802941,
  "peak_wheel_torque_nm": 0.20059090852737427,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.640573495009448
}
```
