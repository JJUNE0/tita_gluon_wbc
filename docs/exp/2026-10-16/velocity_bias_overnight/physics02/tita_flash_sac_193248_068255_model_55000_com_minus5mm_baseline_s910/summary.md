# tita_flash_sac_193248_068255_model_55000_com_minus5mm_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_com_minus5mm_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
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
  "initial_physics_sha256": "72f0fee3c2e3ef55e5cf7cd150a831ec5946f0d8e64c312e9bfba56c9920461f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 15.13110294898379,
  "max_drift_m": 15.13110294898379,
  "radial_IAE_m_s": 427.05873940960555,
  "signed_longitudinal_delta_m": 14.936034622241241,
  "tail_speed_mean_m_s": 0.2747611727734662,
  "tail_speed_rms_m_s": 0.27476127987454396,
  "tail_sensor_speed_mean_m_s": 0.2741677693157092,
  "tail_fk_speed_mean_m_s": 0.27415917724288563,
  "peak_tilt_rad": 0.164725687967332,
  "peak_wheel_torque_nm": 0.26621246337890625,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 14.771300613996573
}
```
