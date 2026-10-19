# tita_flash_sac_193248_068255_model_65000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
    },
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
  "initial_physics_sha256": "a78864b3a81899d2cc35b1666eee42dc7017e4b0b532d082a8a12c602d0f8a29",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05226684608345363,
  "max_drift_m": 0.08946651369757345,
  "radial_IAE_m_s": 3.1367514491735715,
  "signed_longitudinal_delta_m": -0.05226441424320133,
  "tail_speed_mean_m_s": -1.7915380909842048e-07,
  "tail_speed_rms_m_s": 1.898746060581553e-07,
  "tail_sensor_speed_mean_m_s": -1.3122089581410875e-07,
  "tail_fk_speed_mean_m_s": 2.1209424786884785e-08,
  "peak_tilt_rad": 0.16062478372943478,
  "peak_wheel_torque_nm": 1.519466519355774,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5460792087534149,
  "final_integral_m_s": -0.5460792191272784,
  "elapsed_wall_s": 15.738522857020143
}
```
