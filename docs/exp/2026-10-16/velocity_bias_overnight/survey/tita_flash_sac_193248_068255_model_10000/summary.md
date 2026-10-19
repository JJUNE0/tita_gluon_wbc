# tita_flash_sac_193248_068255_model_10000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "856e10371292129ee53a09dde9277620a11f5c7406541f514eb533e2b37874f8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.33785795475868896,
  "max_drift_m": 0.33785795475868896,
  "radial_IAE_m_s": 9.503315074524362,
  "signed_longitudinal_delta_m": 0.33338462872553826,
  "tail_speed_mean_m_s": 0.0063720201239955004,
  "tail_speed_rms_m_s": 0.006375319558699124,
  "tail_sensor_speed_mean_m_s": 0.006378831667662451,
  "tail_fk_speed_mean_m_s": 0.006385832032824251,
  "peak_tilt_rad": 0.02448153183253613,
  "peak_wheel_torque_nm": 0.2685118317604065,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.418456994986627
}
```
