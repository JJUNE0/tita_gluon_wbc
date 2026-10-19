# tita_flash_sac_193248_068255_model_80000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": 0.2,
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
  "initial_physics_sha256": "73779233c3daf03f6166c53c1f8e473321e51a771b4f3b3329052be8965f8eba",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.848704139790464,
  "max_drift_m": 2.848704139790464,
  "radial_IAE_m_s": 87.57757144212496,
  "signed_longitudinal_delta_m": 2.8467554871144944,
  "tail_speed_mean_m_s": 0.048319710878171565,
  "tail_speed_rms_m_s": 0.048415316955203784,
  "tail_sensor_speed_mean_m_s": 0.048047724294673876,
  "tail_fk_speed_mean_m_s": 0.048231055133840524,
  "peak_tilt_rad": 0.06148018885492079,
  "peak_wheel_torque_nm": 2.228168487548828,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.716123295016587
}
```
