# tita_flash_sac_193248_068255_model_20000_nominal_fk

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_nominal_fk",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "estimator": "fk",
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
  "final_drift_m": 0.06537824643176253,
  "max_drift_m": 0.09354606567973875,
  "radial_IAE_m_s": 3.9514194664492654,
  "signed_longitudinal_delta_m": 0.06537680561152283,
  "tail_speed_mean_m_s": -1.3020316825549895e-05,
  "tail_speed_rms_m_s": 1.3025393562539607e-05,
  "tail_sensor_speed_mean_m_s": -1.0803526756498956e-05,
  "tail_fk_speed_mean_m_s": -4.409319272800093e-06,
  "peak_tilt_rad": 0.1557086751603045,
  "peak_wheel_torque_nm": 1.651629090309143,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.68771944054341,
  "final_integral_m_s": 0.6877281909103343,
  "elapsed_wall_s": 14.01017722103279
}
```
