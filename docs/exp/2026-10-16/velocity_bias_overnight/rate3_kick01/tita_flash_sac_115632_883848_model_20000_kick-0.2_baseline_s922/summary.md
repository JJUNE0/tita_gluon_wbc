# tita_flash_sac_115632_883848_model_20000_kick-0.2_baseline_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick-0.2_baseline_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": false,
    "kick": -0.2,
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
  "initial_physics_sha256": "38daf7dfacfefd017439762baa95ecd948387cb034fa0fdc0b2bbc789804fca1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 14.197298069917283,
  "max_drift_m": 14.197298069917283,
  "radial_IAE_m_s": 422.37456127765154,
  "signed_longitudinal_delta_m": 13.678139661896312,
  "tail_speed_mean_m_s": 0.245443411474221,
  "tail_speed_rms_m_s": 0.2454434116199734,
  "tail_sensor_speed_mean_m_s": 0.24491393263379926,
  "tail_fk_speed_mean_m_s": 0.24488330761835517,
  "peak_tilt_rad": 0.17105284913938767,
  "peak_wheel_torque_nm": 1.2370457649230957,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.888713216001634
}
```
