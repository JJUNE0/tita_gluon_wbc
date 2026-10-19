# tita_flash_sac_193248_068255_model_25000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
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
  "initial_physics_sha256": "36b5ef16355db90d8755bfa241c22cf4b09131bf05cd8cc33adbb2bbd846b42b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 11.325779534620153,
  "max_drift_m": 11.325779534620153,
  "radial_IAE_m_s": 341.1789772347662,
  "signed_longitudinal_delta_m": 11.325770507177984,
  "tail_speed_mean_m_s": 0.18747772336339397,
  "tail_speed_rms_m_s": 0.18747775770551378,
  "tail_sensor_speed_mean_m_s": 0.18707182623109603,
  "tail_fk_speed_mean_m_s": 0.18707173314848347,
  "peak_tilt_rad": 0.10857293952996461,
  "peak_wheel_torque_nm": 0.02682316303253174,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.379475280991755
}
```
