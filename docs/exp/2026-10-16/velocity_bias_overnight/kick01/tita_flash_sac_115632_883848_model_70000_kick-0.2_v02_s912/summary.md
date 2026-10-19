# tita_flash_sac_115632_883848_model_70000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "7d856be8bd0ab717e7ac196bb06f510bc9e960d7b5cf3dadca39d9e300a5dbaf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013360731374086589,
  "max_drift_m": 0.0947180414021105,
  "radial_IAE_m_s": 0.8663354977735798,
  "signed_longitudinal_delta_m": -0.013330188111946004,
  "tail_speed_mean_m_s": 1.3317992047302334e-06,
  "tail_speed_rms_m_s": 2.3417013051984856e-06,
  "tail_sensor_speed_mean_m_s": 1.2848194254005894e-06,
  "tail_fk_speed_mean_m_s": 1.3442166924831577e-06,
  "peak_tilt_rad": 0.12256413526424792,
  "peak_wheel_torque_nm": 1.947396159172058,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12475973296440779,
  "final_integral_m_s": -0.12475972169887654,
  "elapsed_wall_s": 13.804144668043591
}
```
