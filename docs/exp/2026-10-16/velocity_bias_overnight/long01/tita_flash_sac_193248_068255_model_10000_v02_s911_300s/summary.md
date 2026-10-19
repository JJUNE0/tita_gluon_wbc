# tita_flash_sac_193248_068255_model_10000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "607d62aa3093fa9304b1a9107d87477cd111e810925c740ef6c6be07557f05e1",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01989411009909538,
  "max_drift_m": 0.01989411009909538,
  "radial_IAE_m_s": 4.335255826086964,
  "signed_longitudinal_delta_m": 0.01716885624698946,
  "tail_speed_mean_m_s": 3.139937748141289e-05,
  "tail_speed_rms_m_s": 3.139978102681137e-05,
  "tail_sensor_speed_mean_m_s": 3.266400684039224e-05,
  "tail_fk_speed_mean_m_s": 3.701672837074413e-05,
  "peak_tilt_rad": 0.027643508185658083,
  "peak_wheel_torque_nm": 0.8957921266555786,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.23919445099290898,
  "final_integral_m_s": 0.23912055367232607,
  "elapsed_wall_s": 65.7153181519825
}
```
