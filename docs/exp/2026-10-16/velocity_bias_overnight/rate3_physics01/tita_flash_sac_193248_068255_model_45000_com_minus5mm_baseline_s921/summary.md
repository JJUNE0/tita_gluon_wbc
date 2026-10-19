# tita_flash_sac_193248_068255_model_45000_com_minus5mm_baseline_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com_minus5mm_baseline_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": false,
    "physics": {
      "com": -0.005
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "a21f1d3c1dba471c0dded9cf61698f4d675794c00310c613db075ac3e942e04c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 9.722743015971046,
  "max_drift_m": 9.722743015971046,
  "radial_IAE_m_s": 288.9761256176339,
  "signed_longitudinal_delta_m": -9.65655088769592,
  "tail_speed_mean_m_s": -0.164896043938069,
  "tail_speed_rms_m_s": 0.16489656928202967,
  "tail_sensor_speed_mean_m_s": -0.16465208418404395,
  "tail_fk_speed_mean_m_s": -0.1646647484260308,
  "peak_tilt_rad": 0.03405886483801046,
  "peak_wheel_torque_nm": 0.18188929557800293,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.232117108011153
}
```
