# tita_flash_sac_193248_068255_model_80000_baseline_s911_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_baseline_s911_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 911,
    "estimator": "fk",
    "runtime": false,
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
  "initial_physics_sha256": "054539ec8e5f9e05227f2c5d4d2b8669245f573099fc676cb91a6b7045d8eb4e",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 16.295665100729625,
  "max_drift_m": 16.295665100729625,
  "radial_IAE_m_s": 2284.93267489524,
  "signed_longitudinal_delta_m": 16.279974279611533,
  "tail_speed_mean_m_s": 0.06041316566252218,
  "tail_speed_rms_m_s": 0.060483762510051185,
  "tail_sensor_speed_mean_m_s": 0.0595643497119316,
  "tail_fk_speed_mean_m_s": 0.06035213352392524,
  "peak_tilt_rad": 0.05540749332253747,
  "peak_wheel_torque_nm": 2.201249122619629,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 55.87468287697993
}
```
