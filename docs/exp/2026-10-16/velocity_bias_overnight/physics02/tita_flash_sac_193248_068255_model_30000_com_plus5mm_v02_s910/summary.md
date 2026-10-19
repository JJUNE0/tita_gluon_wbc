# tita_flash_sac_193248_068255_model_30000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "a31b0b69ca60fccd3d4e267cf6ea8789af0d546294e71b2154abce7d30072e7a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014293491335644913,
  "max_drift_m": 0.02511898002850663,
  "radial_IAE_m_s": 0.864182414262338,
  "signed_longitudinal_delta_m": 0.014287375600517944,
  "tail_speed_mean_m_s": -1.6553251307424557e-06,
  "tail_speed_rms_m_s": 2.3000155496241574e-06,
  "tail_sensor_speed_mean_m_s": -1.4192230137556462e-06,
  "tail_fk_speed_mean_m_s": -1.666415541467113e-06,
  "peak_tilt_rad": 0.029135742183428848,
  "peak_wheel_torque_nm": 0.5104432106018066,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.14973068472171394,
  "final_integral_m_s": 0.14974477973242176,
  "elapsed_wall_s": 18.85674001002917
}
```
