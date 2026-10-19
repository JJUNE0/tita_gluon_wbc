# tita_flash_sac_193248_068255_model_55000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_55000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_55000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 920,
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
  "checkpoint_sha256": "02d44258f752e3d43bac0b8eba0ebb2b4c1d262d812cc040b22672a16cdb583c",
  "onnx_sha256": "98bc9d9fb343d683cc0b87892391ac7fee7f391381ceff241490864772abca13",
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
  "initial_physics_sha256": "d3f04824438473ba2176fa9409a428f7c0a91c7c351068a053832b5757ba1ad8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.023689326339518216,
  "max_drift_m": 0.07608310394965415,
  "radial_IAE_m_s": 1.8425844832335208,
  "signed_longitudinal_delta_m": -0.023687428022048086,
  "tail_speed_mean_m_s": 0.00021555331378979027,
  "tail_speed_rms_m_s": 0.00021556884942650601,
  "tail_sensor_speed_mean_m_s": 0.00021566719572986773,
  "tail_fk_speed_mean_m_s": 0.00021401372063944014,
  "peak_tilt_rad": 0.13794802009204932,
  "peak_wheel_torque_nm": 0.9178454279899597,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.30884119693865153,
  "final_integral_m_s": 0.30884119693865153,
  "elapsed_wall_s": 12.529267123027239
}
```
