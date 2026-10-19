# tita_flash_sac_193248_068255_model_45000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "5bdcd5e3797b940c8b5d89a4921634443eec5f551a10d2cf9b60caca7d4c0028",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.722743724379212,
  "max_drift_m": 9.722743724379212,
  "radial_IAE_m_s": 288.9761569343017,
  "signed_longitudinal_delta_m": -9.656551586786186,
  "tail_speed_mean_m_s": -0.16489605246985298,
  "tail_speed_rms_m_s": 0.16489657780251984,
  "tail_sensor_speed_mean_m_s": -0.1646520948148769,
  "tail_fk_speed_mean_m_s": -0.16466475715731868,
  "peak_tilt_rad": 0.034058868279507104,
  "peak_wheel_torque_nm": 0.18189746141433716,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 12.991039387008641
}
```
