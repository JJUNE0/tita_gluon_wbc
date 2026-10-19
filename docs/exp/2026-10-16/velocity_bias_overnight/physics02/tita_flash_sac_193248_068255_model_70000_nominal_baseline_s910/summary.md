# tita_flash_sac_193248_068255_model_70000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "fbb91a77f94663190743d3493d38173b921d3686d5339a24bd96ed626c1c79d6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.0001892978576117,
  "max_drift_m": 3.0001892978576117,
  "radial_IAE_m_s": 83.1168965792408,
  "signed_longitudinal_delta_m": 2.9989970248509694,
  "tail_speed_mean_m_s": 0.05696562099903646,
  "tail_speed_rms_m_s": 0.056984520225206135,
  "tail_sensor_speed_mean_m_s": 0.05684296361859579,
  "tail_fk_speed_mean_m_s": 0.05684139306239694,
  "peak_tilt_rad": 0.08422855083554404,
  "peak_wheel_torque_nm": 0.05784301459789276,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 9.77700023399666
}
```
