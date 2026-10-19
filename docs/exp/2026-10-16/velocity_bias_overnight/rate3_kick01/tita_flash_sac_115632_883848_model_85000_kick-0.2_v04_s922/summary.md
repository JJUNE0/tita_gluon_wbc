# tita_flash_sac_115632_883848_model_85000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: d1530cc4acd3186dfa88b59087ef850fd51f024ba7eba3252bc14a6549cc77d7

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_85000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_85000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": -0.2,
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
  "initial_physics_sha256": "2bfeabc1537c55824be13d42ddebf8f64a497ed37c5f14330e0695fc7063c8e2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.09326280232821,
  "max_drift_m": 0.10518477095788653,
  "radial_IAE_m_s": 5.441729657647855,
  "signed_longitudinal_delta_m": 0.09326116018132147,
  "tail_speed_mean_m_s": -5.7524413723221e-06,
  "tail_speed_rms_m_s": 1.0201726598800273e-05,
  "tail_sensor_speed_mean_m_s": -5.700653854859594e-06,
  "tail_fk_speed_mean_m_s": -5.40438317934601e-06,
  "peak_tilt_rad": 0.06447540463391599,
  "peak_wheel_torque_nm": 1.8799864053726196,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5825157237221376,
  "final_integral_m_s": 0.5825157237221376,
  "elapsed_wall_s": 6.43833892402472
}
```
