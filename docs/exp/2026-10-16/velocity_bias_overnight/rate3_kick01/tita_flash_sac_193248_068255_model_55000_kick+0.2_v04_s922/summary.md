# tita_flash_sac_193248_068255_model_55000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
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
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "57c61505286d4a3da74c63710e227896c73e09ae07d0c507a88658563665b65b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02133491778617348,
  "max_drift_m": 0.1862400157147659,
  "radial_IAE_m_s": 1.890588637032149,
  "signed_longitudinal_delta_m": -0.021333605826029556,
  "tail_speed_mean_m_s": 0.00021089690592464852,
  "tail_speed_rms_m_s": 0.0002110429050560703,
  "tail_sensor_speed_mean_m_s": 0.000210867727547531,
  "tail_fk_speed_mean_m_s": 0.00020935301846546558,
  "peak_tilt_rad": 0.16144230702171858,
  "peak_wheel_torque_nm": 1.6714746952056885,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3129077839349504,
  "final_integral_m_s": 0.3129077839349504,
  "elapsed_wall_s": 7.091823271010071
}
```
