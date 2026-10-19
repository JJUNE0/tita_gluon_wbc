# tita_flash_sac_193248_068255_model_20000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_20000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_20000",
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
  "checkpoint_sha256": "4bb0e92e03390c3256497280f4ab3eda89d64ce8dfc23bfd9d799d69aa0d068c",
  "onnx_sha256": "a24d51f2c61ac25fc44c8e657cd90494575b17855d820a382e66b027caddbaac",
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
  "initial_physics_sha256": "3980a885ba9da9ed840f9667359e3e87fad91acece906ac76ba39d3f7e7fa7d2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013283893103319733,
  "max_drift_m": 0.07580059486601123,
  "radial_IAE_m_s": 0.9480719904238623,
  "signed_longitudinal_delta_m": 0.013264159817659767,
  "tail_speed_mean_m_s": -3.908456369199026e-05,
  "tail_speed_rms_m_s": 3.908793269403083e-05,
  "tail_sensor_speed_mean_m_s": -2.3580339975212517e-05,
  "tail_fk_speed_mean_m_s": -1.3795777502497483e-05,
  "peak_tilt_rad": 0.15069002062963355,
  "peak_wheel_torque_nm": 1.8430960178375244,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.6749749077220594,
  "final_integral_m_s": 0.6749749077220594,
  "elapsed_wall_s": 12.902476772957016
}
```
