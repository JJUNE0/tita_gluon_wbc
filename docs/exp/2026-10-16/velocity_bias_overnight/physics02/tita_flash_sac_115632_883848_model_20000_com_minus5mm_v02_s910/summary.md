# tita_flash_sac_115632_883848_model_20000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": -0.005
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
  "final_drift_m": 0.01847385926591986,
  "max_drift_m": 0.053036381227798454,
  "radial_IAE_m_s": 1.0983407601078614,
  "signed_longitudinal_delta_m": 0.018451984769930128,
  "tail_speed_mean_m_s": 2.9190788124994378e-05,
  "tail_speed_rms_m_s": 2.945438125355055e-05,
  "tail_sensor_speed_mean_m_s": 3.5043072126591595e-05,
  "tail_fk_speed_mean_m_s": 4.158826834964646e-05,
  "peak_tilt_rad": 0.14180897853272212,
  "peak_wheel_torque_nm": 0.9205952286720276,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21192170018227718,
  "final_integral_m_s": 0.211850705931771,
  "elapsed_wall_s": 12.729088493040763
}
```
