# tita_flash_sac_115632_883848_model_20000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "ab04ab81bc0501c9010f0e29b4a07277dbfc9474ba7bb0e9499d8314d61b9867",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02339902352682452,
  "max_drift_m": 0.07070677805514881,
  "radial_IAE_m_s": 1.4698638935004182,
  "signed_longitudinal_delta_m": 0.023372144227278784,
  "tail_speed_mean_m_s": -1.7200652699331196e-05,
  "tail_speed_rms_m_s": 1.895138543606965e-05,
  "tail_sensor_speed_mean_m_s": 1.3227662197787851e-05,
  "tail_fk_speed_mean_m_s": 2.3790088840024632e-05,
  "peak_tilt_rad": 0.15294259454728287,
  "peak_wheel_torque_nm": 0.9770207405090332,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.27119251045018017,
  "final_integral_m_s": 0.2711494291697849,
  "elapsed_wall_s": 12.161280580970924
}
```
