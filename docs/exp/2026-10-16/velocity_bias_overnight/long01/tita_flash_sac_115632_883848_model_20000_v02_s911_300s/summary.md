# tita_flash_sac_115632_883848_model_20000_v02_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_v02_s911_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "48fc3376f70f5f4b9c64c8d97b468fcb7386c8555349e912eb02119b467307f6",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.022442078999563072,
  "max_drift_m": 0.07198333396906903,
  "radial_IAE_m_s": 7.185209970425599,
  "signed_longitudinal_delta_m": 0.022280974388325343,
  "tail_speed_mean_m_s": 2.9365444806077717e-05,
  "tail_speed_rms_m_s": 3.0189262962314306e-05,
  "tail_sensor_speed_mean_m_s": -0.00014822600903453085,
  "tail_fk_speed_mean_m_s": 6.380879958796942e-07,
  "peak_tilt_rad": 0.153624718942603,
  "peak_wheel_torque_nm": 1.0060029029846191,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.38437210807464783,
  "final_integral_m_s": 0.38436707272797754,
  "elapsed_wall_s": 65.97102259198437
}
```
