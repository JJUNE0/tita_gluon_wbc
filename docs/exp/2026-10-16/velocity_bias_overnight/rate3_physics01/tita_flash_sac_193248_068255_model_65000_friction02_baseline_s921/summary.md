# tita_flash_sac_193248_068255_model_65000_friction02_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction02_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
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
  "initial_physics_sha256": "d738466f58ab0d549bfb42988ad97bd0e88cf84562c30b161988941283519170",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.1449394465943628,
  "max_drift_m": 2.1449394465943628,
  "radial_IAE_m_s": 64.21045381330279,
  "signed_longitudinal_delta_m": -2.1428069408930797,
  "tail_speed_mean_m_s": -0.03583567420314601,
  "tail_speed_rms_m_s": 0.03583567465858325,
  "tail_sensor_speed_mean_m_s": -0.03576428627820745,
  "tail_fk_speed_mean_m_s": -0.035761550410323376,
  "peak_tilt_rad": 0.02397866288411321,
  "peak_wheel_torque_nm": 0.021902218461036682,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 6.857065509015229
}
```
