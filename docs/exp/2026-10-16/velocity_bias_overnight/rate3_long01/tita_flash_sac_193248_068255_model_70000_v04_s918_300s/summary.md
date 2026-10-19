# tita_flash_sac_193248_068255_model_70000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "37844ec20ef7e72ec50be16c83ce04c85294187e3958769df3b842ee8c41454a",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.0214980588194212,
  "max_drift_m": 0.0214980588194212,
  "radial_IAE_m_s": 4.729484679171726,
  "signed_longitudinal_delta_m": 0.02149592722031066,
  "tail_speed_mean_m_s": 1.7263900425350462e-05,
  "tail_speed_rms_m_s": 1.7265385793602432e-05,
  "tail_sensor_speed_mean_m_s": 1.7252187379595e-05,
  "tail_fk_speed_mean_m_s": 1.684413499880229e-05,
  "peak_tilt_rad": 0.07500607571659601,
  "peak_wheel_torque_nm": 0.0919419452548027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.12386051225186583,
  "final_integral_m_s": 0.12386051225186583,
  "elapsed_wall_s": 26.72735747200204
}
```
