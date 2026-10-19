# tita_flash_sac_115632_883848_model_30000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "433b0dc009f8f2e6cc55a98acc237f30d8321ce446fa326efcb5b8155411e607",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03738996761160713,
  "max_drift_m": 0.06662279294566302,
  "radial_IAE_m_s": 2.2725164851189468,
  "signed_longitudinal_delta_m": 0.037389603559709925,
  "tail_speed_mean_m_s": -8.927510906933064e-06,
  "tail_speed_rms_m_s": 9.181699827408931e-06,
  "tail_sensor_speed_mean_m_s": -8.907913118853704e-06,
  "tail_fk_speed_mean_m_s": -8.81664672270862e-06,
  "peak_tilt_rad": 0.19072483137689344,
  "peak_wheel_torque_nm": 2.1943798065185547,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3383887581879567,
  "final_integral_m_s": -0.3383887581879567,
  "elapsed_wall_s": 10.481519696011674
}
```
