# tita_flash_sac_115632_883848_model_35000_friction08_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 04d8993b85810ece43a5d202a8a86b46097dcc9e30ce2c7825e73f538f9beab6

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_35000_friction08_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 13.7641431336512,
  "max_drift_m": 13.7641431336512,
  "radial_IAE_m_s": 408.76902278439104,
  "signed_longitudinal_delta_m": 13.76161879368908,
  "tail_speed_mean_m_s": 0.2324796418929163,
  "tail_speed_rms_m_s": 0.23247964530638765,
  "tail_sensor_speed_mean_m_s": 0.23197672446876177,
  "tail_fk_speed_mean_m_s": 0.23197479189228665,
  "peak_tilt_rad": 0.14075629447905835,
  "peak_wheel_torque_nm": 0.9009581804275513,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.340939688961953
}
```
