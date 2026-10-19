# tita_flash_sac_115632_883848_model_20000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
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
  "final_drift_m": 0.029183412488926603,
  "max_drift_m": 0.1505347163306871,
  "radial_IAE_m_s": 2.1213275308706248,
  "signed_longitudinal_delta_m": -0.02907263663602348,
  "tail_speed_mean_m_s": -6.421021610546848e-05,
  "tail_speed_rms_m_s": 0.0015736916767055303,
  "tail_sensor_speed_mean_m_s": -6.212586539650571e-05,
  "tail_fk_speed_mean_m_s": -5.321640208031246e-05,
  "peak_tilt_rad": 0.17912332799216757,
  "peak_wheel_torque_nm": 2.3428444862365723,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.26995512537453675,
  "final_integral_m_s": 0.26995512537453675,
  "elapsed_wall_s": 10.083191200974397
}
```
