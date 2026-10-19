# tita_flash_sac_115632_883848_model_20000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "6514817c18f02f94e05d5c7210d5da9fceec150eefd9bb9d5cea8ff2928d2dc4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023802118365507764,
  "max_drift_m": 0.07208418057112236,
  "radial_IAE_m_s": 1.466512395978532,
  "signed_longitudinal_delta_m": 0.023802098058983295,
  "tail_speed_mean_m_s": 7.977622805636156e-07,
  "tail_speed_rms_m_s": 3.220931157489312e-06,
  "tail_sensor_speed_mean_m_s": 6.535041136852098e-06,
  "tail_fk_speed_mean_m_s": 1.420385118088667e-05,
  "peak_tilt_rad": 0.15367431347295524,
  "peak_wheel_torque_nm": 1.0077985525131226,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2696391597122154,
  "final_integral_m_s": 0.2696209793865153,
  "elapsed_wall_s": 16.06328395899618
}
```
