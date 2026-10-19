# tita_flash_sac_193248_068255_model_65000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "737bd8e6710f0d3f88dcdfee25eb4df65ec45ef72b0e03582d86a12503af37a7",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.018282843447431602,
  "max_drift_m": 0.027756923546008963,
  "radial_IAE_m_s": 1.1245679389577279,
  "signed_longitudinal_delta_m": -0.01827540271635108,
  "tail_speed_mean_m_s": 1.2931671309127635e-05,
  "tail_speed_rms_m_s": 1.2933359286459104e-05,
  "tail_sensor_speed_mean_m_s": 1.2470167439176266e-05,
  "tail_fk_speed_mean_m_s": 1.3866901761850388e-05,
  "peak_tilt_rad": 0.04938541358800275,
  "peak_wheel_torque_nm": 0.25225117802619934,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1871139633056056,
  "final_integral_m_s": -0.18714095364415148,
  "elapsed_wall_s": 13.899471649026964
}
```
