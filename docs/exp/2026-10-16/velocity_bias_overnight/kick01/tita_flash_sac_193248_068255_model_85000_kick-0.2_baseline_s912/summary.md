# tita_flash_sac_193248_068255_model_85000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_85000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "520e4e186e62e77bd04fecac7cdf45838dad108ef710de3f9088dd03a7b3223b",
  "onnx_sha256": "5d2438e3be90051d15448f31e014bdcdd44f963c2caabea6f5c8a62f0c9e2e0e",
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
  "initial_physics_sha256": "079e3d4eb197d4f613f809616455dc7d9186f54a8ef806877b4b53af65dbb08f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 6.478626139231934,
  "max_drift_m": 6.478626139231934,
  "radial_IAE_m_s": 177.75999322630173,
  "signed_longitudinal_delta_m": 6.475217861447427,
  "tail_speed_mean_m_s": 0.11974306220118136,
  "tail_speed_rms_m_s": 0.11974465929068438,
  "tail_sensor_speed_mean_m_s": 0.11948428544424022,
  "tail_fk_speed_mean_m_s": 0.11948226425190449,
  "peak_tilt_rad": 0.06876882269130324,
  "peak_wheel_torque_nm": 1.6122169494628906,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.547131256957073
}
```
