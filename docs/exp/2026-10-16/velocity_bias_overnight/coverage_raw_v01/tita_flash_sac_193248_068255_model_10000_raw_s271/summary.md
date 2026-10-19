# tita_flash_sac_193248_068255_model_10000_raw_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_raw_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "raw"
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "c225686e07e3554b3507dbb4d3c00e70d440ef5fe7925ef98827da5e222f25ab",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007439174007656557,
  "max_drift_m": 0.008318301213488859,
  "radial_IAE_m_s": 0.17825647294387414,
  "signed_longitudinal_delta_m": -0.007109557619442943,
  "tail_speed_mean_m_s": -0.0003147672431043279,
  "tail_speed_rms_m_s": 0.026424005831886227,
  "tail_sensor_speed_mean_m_s": -0.0002729223226907454,
  "tail_fk_speed_mean_m_s": -1.905973762568745e-05,
  "peak_tilt_rad": 0.05686993449258515,
  "peak_wheel_torque_nm": 1.8632384538650513,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.16584403108909407,
  "final_integral_m_s": -0.027368117952531714,
  "elapsed_wall_s": 4.418300005956553
}
```
