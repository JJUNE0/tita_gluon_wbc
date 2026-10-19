# tita_flash_sac_115632_883848_model_70000_com_plus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_plus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "16e8f2ab65730be3e666e1abe082e14d78007d924e13d9ba4817a4d5b2ce4735",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.009880086544666858,
  "max_drift_m": 0.01921830179488386,
  "radial_IAE_m_s": 0.6110291427087295,
  "signed_longitudinal_delta_m": -0.009869425500368309,
  "tail_speed_mean_m_s": 7.926128467240603e-06,
  "tail_speed_rms_m_s": 7.931654655424758e-06,
  "tail_sensor_speed_mean_m_s": 7.879649070961998e-06,
  "tail_fk_speed_mean_m_s": 7.850110319536314e-06,
  "peak_tilt_rad": 0.033990349576866086,
  "peak_wheel_torque_nm": 0.1542532593011856,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.09041757455466788,
  "final_integral_m_s": -0.09041757455466788,
  "elapsed_wall_s": 5.793843785009813
}
```
