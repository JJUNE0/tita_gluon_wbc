# tita_flash_sac_193248_068255_model_10000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "initial_physics_sha256": "4ec37a130816d7d6d4be2b6de65588fbcac49b09ba5db1f45f9d874915947e5a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02767353100177905,
  "max_drift_m": 0.028497143677568334,
  "radial_IAE_m_s": 1.1318424831599418,
  "signed_longitudinal_delta_m": -0.013752860812569073,
  "tail_speed_mean_m_s": -0.0002488195102144876,
  "tail_speed_rms_m_s": 0.0002687661488222271,
  "tail_sensor_speed_mean_m_s": -0.00041753135601247244,
  "tail_fk_speed_mean_m_s": -0.00030837843983557545,
  "peak_tilt_rad": 0.05850879438179657,
  "peak_wheel_torque_nm": 0.82707279920578,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.41331011726811284,
  "final_integral_m_s": -0.41246154125327417,
  "elapsed_wall_s": 17.427615225024056
}
```
