# tita_flash_sac_193248_068255_model_65000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
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
  "initial_physics_sha256": "985456b0ee02351e499bb72413c138f6504d3c52086b98a538afe20d25075d54",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.144939539845434,
  "max_drift_m": 2.144939539845434,
  "radial_IAE_m_s": 64.21045864945134,
  "signed_longitudinal_delta_m": -2.1428070419597023,
  "tail_speed_mean_m_s": -0.03583566162638327,
  "tail_speed_rms_m_s": 0.0358356620830114,
  "tail_sensor_speed_mean_m_s": -0.035764275053797895,
  "tail_fk_speed_mean_m_s": -0.03576153793482131,
  "peak_tilt_rad": 0.02397865677915112,
  "peak_wheel_torque_nm": 0.021907150745391846,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.433802742976695
}
```
