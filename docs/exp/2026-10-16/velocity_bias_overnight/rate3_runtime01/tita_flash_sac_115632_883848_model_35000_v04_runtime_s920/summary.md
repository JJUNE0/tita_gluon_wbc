# tita_flash_sac_115632_883848_model_35000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "initial_physics_sha256": "614e7db35dd3144bcbdadf615642276d34ac2a9d55cf3bb8b9de7d4a1e6dc854",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024856299513982213,
  "max_drift_m": 0.07168112058848489,
  "radial_IAE_m_s": 1.455305238098262,
  "signed_longitudinal_delta_m": 0.02485629944933074,
  "tail_speed_mean_m_s": 4.7966276708307236e-05,
  "tail_speed_rms_m_s": 4.833704512480928e-05,
  "tail_sensor_speed_mean_m_s": 4.780645515662264e-05,
  "tail_fk_speed_mean_m_s": 5.000557457528409e-05,
  "peak_tilt_rad": 0.136947111595217,
  "peak_wheel_torque_nm": 2.3244094848632812,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6021276638445212,
  "final_integral_m_s": 0.6021276638445212,
  "elapsed_wall_s": 12.739389644993935
}
```
