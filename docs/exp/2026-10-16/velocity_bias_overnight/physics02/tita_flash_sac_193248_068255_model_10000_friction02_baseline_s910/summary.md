# tita_flash_sac_193248_068255_model_10000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
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
  "initial_physics_sha256": "cca919d7f0afb824a6bc8964297181f099cf176af9237b83f8b25fb63d1ade90",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 1.0809674172689177,
  "max_drift_m": 1.0809674172689177,
  "radial_IAE_m_s": 41.794578402008284,
  "signed_longitudinal_delta_m": 0.04129357618060955,
  "tail_speed_mean_m_s": 0.026584344535529963,
  "tail_speed_rms_m_s": 0.02658434456534723,
  "tail_sensor_speed_mean_m_s": 0.02673486729928633,
  "tail_fk_speed_mean_m_s": 0.026802156706675507,
  "peak_tilt_rad": 0.018414101230779467,
  "peak_wheel_torque_nm": 0.5800868272781372,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.036714084038977
}
```
