# tita_flash_sac_193248_068255_model_65000_kick-0.2_v02_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_kick-0.2_v02_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "d1ffb587b3e1db2827ff5262655c37108fe4d9ec91e3d0a7bae949eb0d406f71",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.019569009999381985,
  "max_drift_m": 0.09982248839590667,
  "radial_IAE_m_s": 1.245865581165813,
  "signed_longitudinal_delta_m": -0.019567475743850482,
  "tail_speed_mean_m_s": 1.2529942264746338e-05,
  "tail_speed_rms_m_s": 1.2531695317490343e-05,
  "tail_sensor_speed_mean_m_s": 1.210627640965251e-05,
  "tail_fk_speed_mean_m_s": 1.3471185086288235e-05,
  "peak_tilt_rad": 0.11970642459259317,
  "peak_wheel_torque_nm": 1.9168959856033325,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18553484845590365,
  "final_integral_m_s": -0.18556118439864003,
  "elapsed_wall_s": 13.693142762000207
}
```
