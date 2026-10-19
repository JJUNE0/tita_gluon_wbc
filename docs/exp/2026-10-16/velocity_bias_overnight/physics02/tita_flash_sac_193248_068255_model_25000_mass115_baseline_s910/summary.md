# tita_flash_sac_193248_068255_model_25000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "352338f6f2755799caee10537c323fc2b8b30ff6a7895d5b824a876f9a5e0508",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 3.5117520030725995,
  "max_drift_m": 3.5117520030725995,
  "radial_IAE_m_s": 110.81557255432634,
  "signed_longitudinal_delta_m": 3.507844461794578,
  "tail_speed_mean_m_s": 0.05287920999954177,
  "tail_speed_rms_m_s": 0.052891551740715484,
  "tail_sensor_speed_mean_m_s": 0.05276562100215108,
  "tail_fk_speed_mean_m_s": 0.05276585041112314,
  "peak_tilt_rad": 0.10928478476672976,
  "peak_wheel_torque_nm": 0.14876049757003784,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.737860692024697
}
```
