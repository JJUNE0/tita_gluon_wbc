# tita_flash_sac_193248_068255_model_20000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "ed298628c9ae96446db4aee1778f92430576de8632c4fbc14e1bfc0ca6a6ece5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003299957930288087,
  "max_drift_m": 0.012391804665393134,
  "radial_IAE_m_s": 0.20327015792059955,
  "signed_longitudinal_delta_m": -0.003296746502235276,
  "tail_speed_mean_m_s": -1.2795862634913124e-06,
  "tail_speed_rms_m_s": 1.4791523751392826e-06,
  "tail_sensor_speed_mean_m_s": -7.942834813249652e-07,
  "tail_fk_speed_mean_m_s": -3.4491169742788917e-07,
  "peak_tilt_rad": 0.17124858028872247,
  "peak_wheel_torque_nm": 0.42321544885635376,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.09733649967657824,
  "final_integral_m_s": -0.09733649967657824,
  "elapsed_wall_s": 9.214832862024195
}
```
