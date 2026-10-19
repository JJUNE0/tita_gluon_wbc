# tita_flash_sac_193248_068255_model_65000_mass130_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass130_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "mass": 1.3
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
  "initial_physics_sha256": "2064e160e4811ea500e2fae8200d5220a21d1278896e92365cc992e33ebc05f0",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.943935855780976,
  "max_drift_m": 11.943935855780976,
  "radial_IAE_m_s": 358.15437652030295,
  "signed_longitudinal_delta_m": -11.82766772417126,
  "tail_speed_mean_m_s": -0.2001922076929308,
  "tail_speed_rms_m_s": 0.20019222124071934,
  "tail_sensor_speed_mean_m_s": -0.1997730779219975,
  "tail_fk_speed_mean_m_s": -0.19976946027695996,
  "peak_tilt_rad": 0.031140991884528013,
  "peak_wheel_torque_nm": 0.2954375147819519,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.542539343005046
}
```
