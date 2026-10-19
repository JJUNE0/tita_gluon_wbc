# tita_flash_sac_193248_068255_model_45000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
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
  "initial_physics_sha256": "b7897f266ceb5001770ebe5f2e3ad2db4a61cca00a1be0a0984db6d11adca929",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0019761277149824953,
  "max_drift_m": 0.07120972099524342,
  "radial_IAE_m_s": 0.27525754728568874,
  "signed_longitudinal_delta_m": -0.0019757782037094257,
  "tail_speed_mean_m_s": 3.7731138328750936e-06,
  "tail_speed_rms_m_s": 3.775070323648514e-06,
  "tail_sensor_speed_mean_m_s": 4.088161205441907e-06,
  "tail_fk_speed_mean_m_s": 1.750292581008155e-06,
  "peak_tilt_rad": 0.11953084671104497,
  "peak_wheel_torque_nm": 1.1700527667999268,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.42918235653471204,
  "final_integral_m_s": -0.42918235653471204,
  "elapsed_wall_s": 9.448280723008793
}
```
