# tita_flash_sac_115632_883848_model_35000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "812e1d190545365d19927ed761ba531847181dee8ce5839a494794153f29be3b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.026245206675790337,
  "max_drift_m": 0.1430883195241531,
  "radial_IAE_m_s": 1.647193504613255,
  "signed_longitudinal_delta_m": 0.026232750340101862,
  "tail_speed_mean_m_s": 4.483847119587943e-05,
  "tail_speed_rms_m_s": 4.5305135872044404e-05,
  "tail_sensor_speed_mean_m_s": 4.473140239700516e-05,
  "tail_fk_speed_mean_m_s": 4.6882972050100144e-05,
  "peak_tilt_rad": 0.16418607108839867,
  "peak_wheel_torque_nm": 3.5274405479431152,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6027469088898042,
  "final_integral_m_s": 0.6027469088898042,
  "elapsed_wall_s": 9.086586769029964
}
```
