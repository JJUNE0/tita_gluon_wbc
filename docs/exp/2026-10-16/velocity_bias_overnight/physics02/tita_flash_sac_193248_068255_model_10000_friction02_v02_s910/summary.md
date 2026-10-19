# tita_flash_sac_193248_068255_model_10000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "cca919d7f0afb824a6bc8964297181f099cf176af9237b83f8b25fb63d1ade90",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.04232325054735634,
  "max_drift_m": 0.04386328345879381,
  "radial_IAE_m_s": 2.3516827657153105,
  "signed_longitudinal_delta_m": 0.024585590016721663,
  "tail_speed_mean_m_s": 0.00046807468291701294,
  "tail_speed_rms_m_s": 0.0005006322905984995,
  "tail_sensor_speed_mean_m_s": 0.0003377310165484652,
  "tail_fk_speed_mean_m_s": 0.0004334841590966983,
  "peak_tilt_rad": 0.0700902180396985,
  "peak_wheel_torque_nm": 0.5433292388916016,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6738017763790761,
  "final_integral_m_s": 0.6737911384075369,
  "elapsed_wall_s": 18.428637256030925
}
```
