# tita_flash_sac_115632_883848_model_10000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_10000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "48a0379d0b30385cff5ccfe473d0ee136f303e640a505719a82bad5a3e3178a5",
  "onnx_sha256": "06e48800bb84c9f9275464d939d3614105bfbc1bbe6af1e92522c94faa5f1e15",
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
  "initial_physics_sha256": "c2c4013a2a13794880fd0ce245bc18b7a24ff7bd90685d8ef5379d662ad02b79",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09189204663630428,
  "max_drift_m": 0.11351993593824766,
  "radial_IAE_m_s": 5.960319947901804,
  "signed_longitudinal_delta_m": 0.09189132686350635,
  "tail_speed_mean_m_s": -0.0007529688597952384,
  "tail_speed_rms_m_s": 0.017603332866131204,
  "tail_sensor_speed_mean_m_s": -0.0008095760465274181,
  "tail_fk_speed_mean_m_s": -0.0009173807201980653,
  "peak_tilt_rad": 0.11404972309963601,
  "peak_wheel_torque_nm": 2.7231922149658203,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3918742448646263,
  "final_integral_m_s": 0.3918742448646263,
  "elapsed_wall_s": 11.063518860959448
}
```
