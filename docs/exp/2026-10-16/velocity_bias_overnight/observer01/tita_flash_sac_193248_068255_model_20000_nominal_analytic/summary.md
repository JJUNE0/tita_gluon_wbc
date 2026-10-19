# tita_flash_sac_193248_068255_model_20000_nominal_analytic

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_analytic",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "analytic",
    "physics": {},
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "f4ba42dd55eec30abb191e6b8209f4ec6027fc577504faff77667de2ab330e6b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06571872518887348,
  "max_drift_m": 0.09355413841562545,
  "radial_IAE_m_s": 3.97123226988473,
  "signed_longitudinal_delta_m": 0.06571730110303108,
  "tail_speed_mean_m_s": -1.298854455809514e-05,
  "tail_speed_rms_m_s": 1.2993747128657204e-05,
  "tail_sensor_speed_mean_m_s": -1.077494925717798e-05,
  "tail_fk_speed_mean_m_s": -4.4108175385657766e-06,
  "peak_tilt_rad": 0.1557086751358301,
  "peak_wheel_torque_nm": 1.638588786125183,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6877211242739427,
  "final_integral_m_s": 0.6877298502250525,
  "elapsed_wall_s": 14.098566826956812
}
```
