# tita_flash_sac_115632_883848_model_70000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "223ca29bf09101a95dd8d596ea10bb4e5f88dab080dab1b6b51d4066484c19da",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.681336512906938,
  "max_drift_m": 4.681336512906938,
  "radial_IAE_m_s": 138.7399277462344,
  "signed_longitudinal_delta_m": -4.587071305412555,
  "tail_speed_mean_m_s": -0.08090113062402765,
  "tail_speed_rms_m_s": 0.08090185178498087,
  "tail_sensor_speed_mean_m_s": -0.08079820110427048,
  "tail_fk_speed_mean_m_s": -0.08079404154355146,
  "peak_tilt_rad": 0.01662216188440535,
  "peak_wheel_torque_nm": 0.1144055724143982,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.582947087008506
}
```
