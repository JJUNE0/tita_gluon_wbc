# tita_flash_sac_193248_068255_model_20000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "initial_physics_sha256": "32eb33d395ab1db4a49313db0c4b033371796ef1312e6544bd345e25d00b93ad",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.011183152019232263,
  "max_drift_m": 0.07576694538923497,
  "radial_IAE_m_s": 3.3472265529471397,
  "signed_longitudinal_delta_m": 0.004553126810865382,
  "tail_speed_mean_m_s": -7.903684196788402e-05,
  "tail_speed_rms_m_s": 8.010632836223338e-05,
  "tail_sensor_speed_mean_m_s": -6.727115649028584e-05,
  "tail_fk_speed_mean_m_s": -5.1893608847217806e-05,
  "peak_tilt_rad": 0.15053981562846142,
  "peak_wheel_torque_nm": 1.8426120281219482,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6493206472787089,
  "final_integral_m_s": 0.6493206472787089,
  "elapsed_wall_s": 51.25044371205149
}
```
