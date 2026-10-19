# tita_flash_sac_193248_068255_model_25000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "final_drift_m": 0.0376337704842857,
  "max_drift_m": 0.08661769831576054,
  "radial_IAE_m_s": 2.3438577850729474,
  "signed_longitudinal_delta_m": 0.03762870180316075,
  "tail_speed_mean_m_s": -3.140327549533117e-05,
  "tail_speed_rms_m_s": 3.150560531275836e-05,
  "tail_sensor_speed_mean_m_s": -3.0849598392605366e-05,
  "tail_fk_speed_mean_m_s": -3.087207623589714e-05,
  "peak_tilt_rad": 0.11087631438032841,
  "peak_wheel_torque_nm": 1.2190897464752197,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.4018242863424662,
  "final_integral_m_s": 0.40188842861333196,
  "elapsed_wall_s": 16.403425841010176
}
```
