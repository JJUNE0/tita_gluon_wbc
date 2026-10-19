# tita_flash_sac_115632_883848_model_55000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: bb5591e26f71829becb4dab5c4e2effcd37054b9722c650dbf0e2ba993329aa7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_55000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_55000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
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
  "initial_physics_sha256": "ea08b03a912c26111a1e46d653f939a69fe8a85c8579c26164e798cb260dfba4",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.016943194373109583,
  "max_drift_m": 0.04571212812682098,
  "radial_IAE_m_s": 3.7127977984529554,
  "signed_longitudinal_delta_m": -0.016407936506018322,
  "tail_speed_mean_m_s": -1.1177542432095604e-05,
  "tail_speed_rms_m_s": 1.1203498166003768e-05,
  "tail_sensor_speed_mean_m_s": -1.146638937789831e-05,
  "tail_fk_speed_mean_m_s": -8.959241965686208e-06,
  "peak_tilt_rad": 0.08949493767047323,
  "peak_wheel_torque_nm": 0.942126989364624,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.20875435940501616,
  "final_integral_m_s": 0.20875435940501616,
  "elapsed_wall_s": 50.069642605027184
}
```
