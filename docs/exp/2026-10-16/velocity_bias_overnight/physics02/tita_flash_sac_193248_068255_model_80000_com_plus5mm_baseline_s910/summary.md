# tita_flash_sac_193248_068255_model_80000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "8e8d230ff99187af5ba390e1c9dd4ee8f289552f99e0e89eb187e4f46b24272a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 5.046768533765411,
  "max_drift_m": 5.046768533765411,
  "radial_IAE_m_s": 144.05627010330187,
  "signed_longitudinal_delta_m": 5.041267438376628,
  "tail_speed_mean_m_s": 0.09076988185434937,
  "tail_speed_rms_m_s": 0.09082396573502326,
  "tail_sensor_speed_mean_m_s": 0.0913267772832833,
  "tail_fk_speed_mean_m_s": 0.09066441973425031,
  "peak_tilt_rad": 0.05784569089033331,
  "peak_wheel_torque_nm": 2.080918312072754,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.655256241967436
}
```
