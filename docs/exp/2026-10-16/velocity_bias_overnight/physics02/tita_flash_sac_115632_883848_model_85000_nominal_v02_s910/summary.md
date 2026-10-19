# tita_flash_sac_115632_883848_model_85000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "09fec977da81e84890525aecb5f25dd4a9b6d648823f9f72f4f27234c44ace1b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05748169095485493,
  "max_drift_m": 0.06583379428026549,
  "radial_IAE_m_s": 3.4360566178496716,
  "signed_longitudinal_delta_m": 0.05747771476413814,
  "tail_speed_mean_m_s": -1.63687921909211e-06,
  "tail_speed_rms_m_s": 4.050497203140948e-06,
  "tail_sensor_speed_mean_m_s": -1.5961412276693712e-06,
  "tail_fk_speed_mean_m_s": -1.2890631036297624e-06,
  "peak_tilt_rad": 0.06542791974248785,
  "peak_wheel_torque_nm": 0.4997304081916809,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5825908174772539,
  "final_integral_m_s": 0.5825823184652101,
  "elapsed_wall_s": 15.624941700021736
}
```
