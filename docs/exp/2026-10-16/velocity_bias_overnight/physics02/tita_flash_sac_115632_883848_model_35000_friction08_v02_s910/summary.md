# tita_flash_sac_115632_883848_model_35000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "47ec173454ec636452acd5552dbc5356a53567e0d32b5302adc13fedf635aa10",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05698989743947541,
  "max_drift_m": 0.07662171806999635,
  "radial_IAE_m_s": 3.385339520554625,
  "signed_longitudinal_delta_m": 0.05698963500506178,
  "tail_speed_mean_m_s": 1.7690724633435885e-05,
  "tail_speed_rms_m_s": 1.786514332789199e-05,
  "tail_sensor_speed_mean_m_s": 1.7418974747233858e-05,
  "tail_fk_speed_mean_m_s": 1.9792148619932038e-05,
  "peak_tilt_rad": 0.13819006226126018,
  "peak_wheel_torque_nm": 1.3171194791793823,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5998976264310301,
  "final_integral_m_s": 0.5998540898304757,
  "elapsed_wall_s": 12.494237356993835
}
```
