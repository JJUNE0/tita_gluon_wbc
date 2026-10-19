# tita_flash_sac_193248_068255_model_65000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "1e74c6c3a68aee300ca75360d8a2240d8d5a23121f2febdab5ddc68677551f26",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.01263280129401819,
  "max_drift_m": 0.034234000525415774,
  "radial_IAE_m_s": 4.47842135529846,
  "signed_longitudinal_delta_m": -0.012554438117803107,
  "tail_speed_mean_m_s": 9.001174437617585e-06,
  "tail_speed_rms_m_s": 9.003123804103683e-06,
  "tail_sensor_speed_mean_m_s": 8.928600148817566e-06,
  "tail_fk_speed_mean_m_s": 9.864577699041066e-06,
  "peak_tilt_rad": 0.04857344849408718,
  "peak_wheel_torque_nm": 0.23521742224693298,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.17108525536549443,
  "final_integral_m_s": -0.17108525536549443,
  "elapsed_wall_s": 26.7897678349982
}
```
