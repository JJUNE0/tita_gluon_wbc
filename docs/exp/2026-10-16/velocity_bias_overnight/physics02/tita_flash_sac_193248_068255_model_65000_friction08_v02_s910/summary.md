# tita_flash_sac_193248_068255_model_65000_friction08_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction08_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.8
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
  "initial_physics_sha256": "cd281ae4b412b510f1e3b82e512c2e3342f34869abcbcf0e5f737bceacf50eba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019470292747683162,
  "max_drift_m": 0.02952064148224161,
  "radial_IAE_m_s": 1.196438757946332,
  "signed_longitudinal_delta_m": -0.0194614060540466,
  "tail_speed_mean_m_s": 1.293135143593587e-05,
  "tail_speed_rms_m_s": 1.2931844210302903e-05,
  "tail_sensor_speed_mean_m_s": 1.391895565478558e-05,
  "tail_fk_speed_mean_m_s": 1.56620625607287e-05,
  "peak_tilt_rad": 0.05081987786119235,
  "peak_wheel_torque_nm": 0.26684391498565674,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1967762175435128,
  "final_integral_m_s": -0.19680518353073662,
  "elapsed_wall_s": 13.717276501003653
}
```
