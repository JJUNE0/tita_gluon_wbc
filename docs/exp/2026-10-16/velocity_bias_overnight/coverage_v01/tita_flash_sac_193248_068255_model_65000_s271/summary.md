# tita_flash_sac_193248_068255_model_65000_s271

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_s271",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 271,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "b362de30fdd9e62a1f854fdf1d858f876767dc623e066b67d2532b09686c0118",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01820216800114373,
  "max_drift_m": 0.02827633725626428,
  "radial_IAE_m_s": 1.1213411994039266,
  "signed_longitudinal_delta_m": -0.01819585411609045,
  "tail_speed_mean_m_s": 1.2910608684628635e-05,
  "tail_speed_rms_m_s": 1.2912292757931524e-05,
  "tail_sensor_speed_mean_m_s": 1.2450081643287957e-05,
  "tail_fk_speed_mean_m_s": 1.3846139980313886e-05,
  "peak_tilt_rad": 0.04959521683159607,
  "peak_wheel_torque_nm": 0.3064287006855011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18695616895426054,
  "final_integral_m_s": -0.18698313202599953,
  "elapsed_wall_s": 4.315376097045373
}
```
