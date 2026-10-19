# tita_flash_sac_193248_068255_model_25000_kick+0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_kick+0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
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
  "initial_physics_sha256": "b9f4e2b0167360c84e21423117cf3c94c082a54caded7add206827ee56e676aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.458540347269542,
  "max_drift_m": 11.458540347269542,
  "radial_IAE_m_s": 348.4578528016001,
  "signed_longitudinal_delta_m": 11.449121850986433,
  "tail_speed_mean_m_s": 0.18763132259306173,
  "tail_speed_rms_m_s": 0.1876313992427861,
  "tail_sensor_speed_mean_m_s": 0.18722510381768223,
  "tail_fk_speed_mean_m_s": 0.1872249922722678,
  "peak_tilt_rad": 0.1279724214560376,
  "peak_wheel_torque_nm": 2.068974018096924,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.898759671952575
}
```
