# tita_flash_sac_193248_068255_model_40000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "093746ff34d942d88dfff97566e14ba718368ac56cc2c6661075034eed94f4b2",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0040530027897035656,
  "max_drift_m": 0.042300807291401836,
  "radial_IAE_m_s": 2.596709120698921,
  "signed_longitudinal_delta_m": -0.004010349546250129,
  "tail_speed_mean_m_s": 8.73755587444839e-06,
  "tail_speed_rms_m_s": 9.152128409861776e-06,
  "tail_sensor_speed_mean_m_s": 9.028876479262035e-06,
  "tail_fk_speed_mean_m_s": 8.574820901758309e-06,
  "peak_tilt_rad": 0.10819184730116649,
  "peak_wheel_torque_nm": 0.8786171674728394,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29319077881335043,
  "final_integral_m_s": 0.29319077881335043,
  "elapsed_wall_s": 50.68463058001362
}
```
