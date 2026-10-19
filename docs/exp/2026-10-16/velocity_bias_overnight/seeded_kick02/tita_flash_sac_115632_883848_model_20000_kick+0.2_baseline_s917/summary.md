# tita_flash_sac_115632_883848_model_20000_kick+0.2_baseline_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick+0.2_baseline_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": false,
    "kick": 0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "8485701f901774b904f060d13e8107bc8d503b35f081e474debf1ecb39f84d80",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.496506202891243,
  "max_drift_m": 14.496506202891243,
  "radial_IAE_m_s": 440.83334674092936,
  "signed_longitudinal_delta_m": 13.924215845909242,
  "tail_speed_mean_m_s": 0.24544194812799475,
  "tail_speed_rms_m_s": 0.2454419482417479,
  "tail_sensor_speed_mean_m_s": 0.2449124634629967,
  "tail_fk_speed_mean_m_s": 0.24488184707040198,
  "peak_tilt_rad": 0.1800378611107487,
  "peak_wheel_torque_nm": 2.2126638889312744,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.947257267020177
}
```
