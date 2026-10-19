# tita_flash_sac_115632_883848_model_35000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "c01ddcbda68e74b8d4adeb98519d14dbb519993944e6647edac1080d5ab564cf",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.02607045585214689,
  "max_drift_m": 0.07155948323451204,
  "radial_IAE_m_s": 7.903361878398887,
  "signed_longitudinal_delta_m": 0.026065075648734972,
  "tail_speed_mean_m_s": -2.8857881913857648e-05,
  "tail_speed_rms_m_s": 2.8923959343946443e-05,
  "tail_sensor_speed_mean_m_s": -2.8480919325654094e-05,
  "tail_fk_speed_mean_m_s": -2.635488131340111e-05,
  "peak_tilt_rad": 0.13696070609152322,
  "peak_wheel_torque_nm": 2.324784278869629,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6080659983326516,
  "final_integral_m_s": 0.6080659983326516,
  "elapsed_wall_s": 54.94682509399718
}
```
