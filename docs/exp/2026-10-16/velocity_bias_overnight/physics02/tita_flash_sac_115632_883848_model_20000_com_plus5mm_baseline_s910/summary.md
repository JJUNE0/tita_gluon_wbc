# tita_flash_sac_115632_883848_model_20000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d4909878277d3c13aa185d3adae77e7883a9250fe22bef90f49a684bb011b3c2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.695543795389186,
  "max_drift_m": 15.695543795389186,
  "radial_IAE_m_s": 475.5246718463687,
  "signed_longitudinal_delta_m": 14.806161223002965,
  "tail_speed_mean_m_s": 0.27002911239372346,
  "tail_speed_rms_m_s": 0.27002911240831606,
  "tail_sensor_speed_mean_m_s": 0.26944614769656094,
  "tail_fk_speed_mean_m_s": 0.26940884589925584,
  "peak_tilt_rad": 0.1770705871062208,
  "peak_wheel_torque_nm": 0.34307366609573364,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.518184401968028
}
```
