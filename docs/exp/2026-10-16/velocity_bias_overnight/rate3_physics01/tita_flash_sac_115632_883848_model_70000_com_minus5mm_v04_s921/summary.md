# tita_flash_sac_115632_883848_model_70000_com_minus5mm_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_com_minus5mm_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "ef57f53e0068d6ce698717127edfeedd794a77c652b08330d2faeb5cf792cfb0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0058752602329874525,
  "max_drift_m": 0.03105395798202822,
  "radial_IAE_m_s": 0.3947577640549068,
  "signed_longitudinal_delta_m": 0.005748415353643403,
  "tail_speed_mean_m_s": -4.053141829802443e-06,
  "tail_speed_rms_m_s": 4.102705215571047e-06,
  "tail_sensor_speed_mean_m_s": -4.100735470927725e-06,
  "tail_fk_speed_mean_m_s": -3.964976109014621e-06,
  "peak_tilt_rad": 0.051610718774834474,
  "peak_wheel_torque_nm": 0.45964285731315613,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.15750819295129714,
  "final_integral_m_s": -0.15750819295129714,
  "elapsed_wall_s": 6.444426280038897
}
```
