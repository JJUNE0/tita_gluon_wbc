# p007_tita_flash_sac_193248_068255_model_20000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "p007_tita_flash_sac_193248_068255_model_20000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "analytic",
    "physics": {
      "mass": 1.3
    },
    "law": {
      "kp": 2.0,
      "ki": 15.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "kp_fast": 3.0
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
  "initial_physics_sha256": "bb5de423d1bc5b38f9ad5544f877dc8ad7f955fb02a7c2ae6b556258a14811e9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05952844711699722,
  "max_drift_m": 0.08160824764276903,
  "radial_IAE_m_s": 1.800829873989716,
  "signed_longitudinal_delta_m": -0.05951900197532761,
  "tail_speed_mean_m_s": -0.0005052507593530878,
  "tail_speed_rms_m_s": 0.13162775656293085,
  "tail_sensor_speed_mean_m_s": 0.00018488481076822566,
  "tail_fk_speed_mean_m_s": -0.00035168838369898584,
  "peak_tilt_rad": 0.32583695529221623,
  "peak_wheel_torque_nm": 2.369797945022583,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03549148819377119,
  "final_integral_m_s": -0.23814833075607555,
  "elapsed_wall_s": 15.3468003179878
}
```
