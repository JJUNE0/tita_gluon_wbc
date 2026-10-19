# tita_flash_sac_115632_883848_model_70000_kick+0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick+0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "57a64db9bd594ad470136146efcfa9d946c1b74fc3cfa8cb08284272c702ba34",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.010556940351696166,
  "max_drift_m": 0.04591366522259772,
  "radial_IAE_m_s": 0.6660202240737128,
  "signed_longitudinal_delta_m": -0.01054542128060217,
  "tail_speed_mean_m_s": 1.863928930364883e-06,
  "tail_speed_rms_m_s": 2.713601974395123e-06,
  "tail_sensor_speed_mean_m_s": 1.8209652513428464e-06,
  "tail_fk_speed_mean_m_s": 1.876209564552174e-06,
  "peak_tilt_rad": 0.046961139131691754,
  "peak_wheel_torque_nm": 1.9689959287643433,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12475894653774568,
  "final_integral_m_s": -0.12475873835688546,
  "elapsed_wall_s": 14.772927716956474
}
```
