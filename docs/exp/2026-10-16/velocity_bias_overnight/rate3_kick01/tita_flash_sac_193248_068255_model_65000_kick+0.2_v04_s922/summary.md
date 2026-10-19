# tita_flash_sac_193248_068255_model_65000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
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
  "initial_physics_sha256": "059b962936652bb0c2f4f3d89537bf233a4e4a2345cb75dd330e79a47b3fcebd",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014938447094314135,
  "max_drift_m": 0.09313165449051808,
  "radial_IAE_m_s": 1.1065830800758631,
  "signed_longitudinal_delta_m": -0.014937907267146156,
  "tail_speed_mean_m_s": 3.359611519469345e-05,
  "tail_speed_rms_m_s": 3.3600134856953184e-05,
  "tail_sensor_speed_mean_m_s": 3.309618187999722e-05,
  "tail_fk_speed_mean_m_s": 3.448490027838283e-05,
  "peak_tilt_rad": 0.05794750101789914,
  "peak_wheel_torque_nm": 1.6940616369247437,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18685781422408518,
  "final_integral_m_s": -0.18685781422408518,
  "elapsed_wall_s": 13.18185724702198
}
```
