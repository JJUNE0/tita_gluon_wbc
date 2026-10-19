# tita_flash_sac_115632_883848_model_70000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "2b59eff138f948c426aa98336a01adaaa5f030e61ce678f789525700cb09c559",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008951927699278649,
  "max_drift_m": 0.013496879206108925,
  "radial_IAE_m_s": 0.5422084964478336,
  "signed_longitudinal_delta_m": -0.008940904887613552,
  "tail_speed_mean_m_s": 2.875271935409059e-06,
  "tail_speed_rms_m_s": 2.878930267921877e-06,
  "tail_sensor_speed_mean_m_s": 2.8346681911659368e-06,
  "tail_fk_speed_mean_m_s": 2.8296810029994795e-06,
  "peak_tilt_rad": 0.034754390181066075,
  "peak_wheel_torque_nm": 0.19011074304580688,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.09087337547106909,
  "final_integral_m_s": -0.09087942383072094,
  "elapsed_wall_s": 12.523211952997372
}
```
