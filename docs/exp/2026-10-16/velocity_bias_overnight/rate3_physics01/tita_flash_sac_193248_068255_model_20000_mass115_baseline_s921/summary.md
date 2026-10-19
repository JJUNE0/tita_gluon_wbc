# tita_flash_sac_193248_068255_model_20000_mass115_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_mass115_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "2f01feda273036b4a10e3a969c0318e094cf64c9501a9857c6f2de2cae2529dd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 4.468073310571759,
  "max_drift_m": 4.468073310571759,
  "radial_IAE_m_s": 134.26958724889855,
  "signed_longitudinal_delta_m": 4.466612079392984,
  "tail_speed_mean_m_s": 0.07418662137650144,
  "tail_speed_rms_m_s": 0.07418664906305673,
  "tail_sensor_speed_mean_m_s": 0.07402777069664229,
  "tail_fk_speed_mean_m_s": 0.07402742114330861,
  "peak_tilt_rad": 0.1469569044988539,
  "peak_wheel_torque_nm": 0.3776363730430603,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.379367957008071
}
```
