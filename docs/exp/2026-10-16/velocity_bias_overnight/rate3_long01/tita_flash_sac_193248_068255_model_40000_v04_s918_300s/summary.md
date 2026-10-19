# tita_flash_sac_193248_068255_model_40000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "final_drift_m": 0.004053176730566705,
  "max_drift_m": 0.042080871749936084,
  "radial_IAE_m_s": 2.5965963843361077,
  "signed_longitudinal_delta_m": -0.004010590296761472,
  "tail_speed_mean_m_s": 8.738498499868368e-06,
  "tail_speed_rms_m_s": 9.156717601726678e-06,
  "tail_sensor_speed_mean_m_s": 9.02786472806615e-06,
  "tail_fk_speed_mean_m_s": 8.575881865274424e-06,
  "peak_tilt_rad": 0.10819184730116649,
  "peak_wheel_torque_nm": 0.8888996839523315,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.29319029860362567,
  "final_integral_m_s": 0.29319029860362567,
  "elapsed_wall_s": 39.00011769402772
}
```
