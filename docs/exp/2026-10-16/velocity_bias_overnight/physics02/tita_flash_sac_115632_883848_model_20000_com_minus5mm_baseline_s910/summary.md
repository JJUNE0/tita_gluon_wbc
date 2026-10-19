# tita_flash_sac_115632_883848_model_20000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "785950021e4a41507c37125c903308c5864852f47e4e80c88c5bb18cac56b847",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.974030358652573,
  "max_drift_m": 12.974030358652573,
  "radial_IAE_m_s": 389.0415494804484,
  "signed_longitudinal_delta_m": 12.71011180733084,
  "tail_speed_mean_m_s": 0.2201788377955787,
  "tail_speed_rms_m_s": 0.22017883809024252,
  "tail_sensor_speed_mean_m_s": 0.21970431033275223,
  "tail_fk_speed_mean_m_s": 0.21968119248769738,
  "peak_tilt_rad": 0.165181374671431,
  "peak_wheel_torque_nm": 0.3674836754798889,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.276000413985457
}
```
