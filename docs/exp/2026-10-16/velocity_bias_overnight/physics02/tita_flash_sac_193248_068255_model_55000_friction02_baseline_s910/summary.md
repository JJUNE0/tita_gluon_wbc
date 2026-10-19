# tita_flash_sac_193248_068255_model_55000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "f81d8a178254e15edbc5681e7834c75977d33580999e8db4d7dcca6f4dc61f60",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 19.446109490398847,
  "max_drift_m": 19.446109490398847,
  "radial_IAE_m_s": 586.8807146035423,
  "signed_longitudinal_delta_m": 19.076619698617087,
  "tail_speed_mean_m_s": 0.3242457774947229,
  "tail_speed_rms_m_s": 0.3242457786107431,
  "tail_sensor_speed_mean_m_s": 0.3235432444688511,
  "tail_fk_speed_mean_m_s": 0.32353651750525575,
  "peak_tilt_rad": 0.1803291108181848,
  "peak_wheel_torque_nm": 0.2004237174987793,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 16.983277664985508
}
```
