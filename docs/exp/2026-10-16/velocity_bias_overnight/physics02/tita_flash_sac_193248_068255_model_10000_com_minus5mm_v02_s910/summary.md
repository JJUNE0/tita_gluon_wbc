# tita_flash_sac_193248_068255_model_10000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "initial_physics_sha256": "94fbf4981b7bd8c4c389e3a3d6752eb085ef6cd5ac13ab9a3115987db4d9a4a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013232734519419628,
  "max_drift_m": 0.013306605592474633,
  "radial_IAE_m_s": 0.7789904252390304,
  "signed_longitudinal_delta_m": -0.013094085913275953,
  "tail_speed_mean_m_s": 1.2743989111096525e-05,
  "tail_speed_rms_m_s": 1.2915762128291504e-05,
  "tail_sensor_speed_mean_m_s": 3.1163120004754424e-05,
  "tail_fk_speed_mean_m_s": 3.8525742278748044e-05,
  "peak_tilt_rad": 0.02417865419566067,
  "peak_wheel_torque_nm": 0.8879533410072327,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.11724992855816932,
  "final_integral_m_s": -0.11733119913175723,
  "elapsed_wall_s": 14.934523272968363
}
```
