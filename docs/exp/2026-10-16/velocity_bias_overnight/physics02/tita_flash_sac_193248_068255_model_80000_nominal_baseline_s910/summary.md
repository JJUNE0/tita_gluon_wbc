# tita_flash_sac_193248_068255_model_80000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "fbc921e7d9f1ecf7c4e0405692dc71c255f8cddfc1b12d0d2818ee98dcba3156",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.529106816845274,
  "max_drift_m": 2.529106816845274,
  "radial_IAE_m_s": 69.74536770046785,
  "signed_longitudinal_delta_m": 2.527376304142297,
  "tail_speed_mean_m_s": 0.04786498052200492,
  "tail_speed_rms_m_s": 0.04796162181914968,
  "tail_sensor_speed_mean_m_s": 0.0480675384700337,
  "tail_fk_speed_mean_m_s": 0.047948251147380896,
  "peak_tilt_rad": 0.054177122024641866,
  "peak_wheel_torque_nm": 2.1976685523986816,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 11.636799731000792
}
```
