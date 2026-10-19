# tita_flash_sac_115632_883848_model_35000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6",
  "onnx_sha256": "3ce2f1cc7a17e8f712ba06efe9dc56bd55d6b0090b07942bae3238a59fef56e0",
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
  "initial_physics_sha256": "e06394447c512896d988591a197bb140f4516a902afe4ec60271beb14a7fd97b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03337858692357658,
  "max_drift_m": 0.04358649324247159,
  "radial_IAE_m_s": 1.97014551760626,
  "signed_longitudinal_delta_m": 0.033378280215811594,
  "tail_speed_mean_m_s": 1.9138061290208665e-05,
  "tail_speed_rms_m_s": 1.916724630921188e-05,
  "tail_sensor_speed_mean_m_s": 1.9255777186389112e-05,
  "tail_fk_speed_mean_m_s": 2.0348986567480903e-05,
  "peak_tilt_rad": 0.1363099844526925,
  "peak_wheel_torque_nm": 1.5126800537109375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3535319950901461,
  "final_integral_m_s": 0.35349347012714644,
  "elapsed_wall_s": 12.753656746994238
}
```
