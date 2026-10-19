# tita_flash_sac_115632_883848_model_85000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
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
  "checkpoint_sha256": "d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7",
  "onnx_sha256": "1ed320e4785fe0edd047b9aa7e4185e975602f208fcf3deca0a9aa486c76114c",
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
  "initial_physics_sha256": "0f7b4498aa7d2094b9217b821088fde011c0e7488480048b94f026bdd5a3f1ee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0033508715339138954,
  "max_drift_m": 0.01686345355767496,
  "radial_IAE_m_s": 0.2238869011839354,
  "signed_longitudinal_delta_m": 0.003332334185341022,
  "tail_speed_mean_m_s": 5.077914349550374e-06,
  "tail_speed_rms_m_s": 6.048781175732719e-06,
  "tail_sensor_speed_mean_m_s": 5.11591962734132e-06,
  "tail_fk_speed_mean_m_s": 5.027957412388948e-06,
  "peak_tilt_rad": 0.07557080711136432,
  "peak_wheel_torque_nm": 0.3505132794380188,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.10713704518139577,
  "final_integral_m_s": -0.10713704518139577,
  "elapsed_wall_s": 9.639185890031513
}
```
