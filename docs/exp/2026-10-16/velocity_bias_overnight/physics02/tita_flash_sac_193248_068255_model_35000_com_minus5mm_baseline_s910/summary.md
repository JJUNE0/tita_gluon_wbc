# tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_35000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_35000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "29db772e13dbcedf2c18de4abb1574229f1744fb03a20ccba615236d504773ae",
  "onnx_sha256": "a1536d3d580cb29e5617b2c1b7c4a7caef45b7730f864b35d9d082a39fc4ebd6",
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
  "initial_physics_sha256": "274ae5e4a6a7583479b050872d07154e2b77447bf14991c21882156d113e516c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 7.163850496376467,
  "max_drift_m": 7.163850496376467,
  "radial_IAE_m_s": 205.72881573524631,
  "signed_longitudinal_delta_m": 7.103798822513341,
  "tail_speed_mean_m_s": 0.1296197785903911,
  "tail_speed_rms_m_s": 0.12962923214724575,
  "tail_sensor_speed_mean_m_s": 0.12934028843522732,
  "tail_fk_speed_mean_m_s": 0.12932434066098822,
  "peak_tilt_rad": 0.06524806426201946,
  "peak_wheel_torque_nm": 0.12604478001594543,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.926322791026905
}
```
