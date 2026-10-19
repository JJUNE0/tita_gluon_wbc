# tita_flash_sac_193248_068255_model_25000_com_plus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_com_plus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "7eab864e636ab5f317176435b8eee773428434d3cc5d9dc69bdf17ef3ac05a10",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 12.311798899238147,
  "max_drift_m": 12.311798899238147,
  "radial_IAE_m_s": 371.10107750615623,
  "signed_longitudinal_delta_m": 12.288601145547315,
  "tail_speed_mean_m_s": 0.20348176864743184,
  "tail_speed_rms_m_s": 0.2034818221858815,
  "tail_sensor_speed_mean_m_s": 0.20304125048335542,
  "tail_fk_speed_mean_m_s": 0.20304123837695612,
  "peak_tilt_rad": 0.11170017794690268,
  "peak_wheel_torque_nm": 0.11644399166107178,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.576774923014455
}
```
