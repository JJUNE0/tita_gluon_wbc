# tita_flash_sac_115632_883848_model_35000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
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
  "initial_physics_sha256": "638c1fc324a3decaa9cc592c3734d1953e81c58af5d0025976bc12b8b682d03c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05597620372748205,
  "max_drift_m": 0.05798681792474549,
  "radial_IAE_m_s": 3.290373279515749,
  "signed_longitudinal_delta_m": 0.055975363686393324,
  "tail_speed_mean_m_s": 1.7969408437817517e-05,
  "tail_speed_rms_m_s": 1.8123041729520527e-05,
  "tail_sensor_speed_mean_m_s": 1.7868393676048126e-05,
  "tail_fk_speed_mean_m_s": 2.007457761877215e-05,
  "peak_tilt_rad": 0.1265695105987461,
  "peak_wheel_torque_nm": 1.5676478147506714,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5842550065283244,
  "final_integral_m_s": 0.5842201348947343,
  "elapsed_wall_s": 12.350061656965408
}
```
