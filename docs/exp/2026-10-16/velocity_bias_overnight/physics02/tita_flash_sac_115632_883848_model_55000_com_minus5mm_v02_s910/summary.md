# tita_flash_sac_115632_883848_model_55000_com_minus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_com_minus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "299f516a6a34c8104584f01da3b34c594b40dc0f79a7e2339f36bfa0e2a84caf",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017746120602045865,
  "max_drift_m": 0.035698888455868945,
  "radial_IAE_m_s": 1.1208404353757975,
  "signed_longitudinal_delta_m": 0.017692653015543392,
  "tail_speed_mean_m_s": -1.9936256205179573e-05,
  "tail_speed_rms_m_s": 1.997753174484716e-05,
  "tail_sensor_speed_mean_m_s": -1.770145586908615e-05,
  "tail_fk_speed_mean_m_s": -1.3967198157388261e-05,
  "peak_tilt_rad": 0.08627281997377145,
  "peak_wheel_torque_nm": 0.8279815912246704,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.19589948235253696,
  "final_integral_m_s": 0.19592988486486004,
  "elapsed_wall_s": 18.156579682021402
}
```
