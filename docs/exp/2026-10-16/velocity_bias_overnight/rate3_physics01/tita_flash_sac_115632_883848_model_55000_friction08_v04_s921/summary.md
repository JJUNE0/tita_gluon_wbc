# tita_flash_sac_115632_883848_model_55000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
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
  "checkpoint_sha256": "bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7",
  "onnx_sha256": "8e2044f08b14f84be2b6152fb6085b58a0f6e377394a8fa0f7c69ebac1c08718",
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
  "initial_physics_sha256": "b334fc3361da69b275cb1ec9deb29e3cefb52062345ceaee5f0650f62d36f3b2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.00625262104186509,
  "max_drift_m": 0.04278552715774403,
  "radial_IAE_m_s": 0.4242180055038425,
  "signed_longitudinal_delta_m": -0.006252604606574872,
  "tail_speed_mean_m_s": -5.012249606825232e-05,
  "tail_speed_rms_m_s": 5.0194983535240976e-05,
  "tail_sensor_speed_mean_m_s": -4.127444601704008e-05,
  "tail_fk_speed_mean_m_s": -3.770244863966907e-05,
  "peak_tilt_rad": 0.08760112305209011,
  "peak_wheel_torque_nm": 0.8396574258804321,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24042575447611575,
  "final_integral_m_s": 0.24042575447611575,
  "elapsed_wall_s": 8.685493635945022
}
```
