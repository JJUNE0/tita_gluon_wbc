# tita_flash_sac_193248_068255_model_45000_nominal_baseline_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_nominal_baseline_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {},
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
  "initial_physics_sha256": "cfc367b42da15abf9f51d7d20cc83e87b54f001e23dd44e02cae134e79b836f6",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.235272246468785,
  "max_drift_m": 8.235272246468785,
  "radial_IAE_m_s": 242.63274375317351,
  "signed_longitudinal_delta_m": -8.19121408359767,
  "tail_speed_mean_m_s": -0.14157669109959162,
  "tail_speed_rms_m_s": 0.14157937331950832,
  "tail_sensor_speed_mean_m_s": -0.14137200317236812,
  "tail_fk_speed_mean_m_s": -0.14138433833729935,
  "peak_tilt_rad": 0.039773324261442644,
  "peak_wheel_torque_nm": 0.19177934527397156,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 4.312523645989131
}
```
