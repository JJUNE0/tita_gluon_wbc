# tita_flash_sac_115632_883848_model_70000_kick-0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_kick-0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "7469e26797ab91b47f24a46aa46d6934b94cca250ce9bafc005fdc4af4f19d85",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.003017013190094343,
  "max_drift_m": 0.11980514108949138,
  "radial_IAE_m_s": 0.4405416111727607,
  "signed_longitudinal_delta_m": -0.0028790260989371257,
  "tail_speed_mean_m_s": 3.1312535003479475e-06,
  "tail_speed_rms_m_s": 5.811776904884165e-06,
  "tail_sensor_speed_mean_m_s": 3.0806501299959683e-06,
  "tail_fk_speed_mean_m_s": 3.1396614784927945e-06,
  "peak_tilt_rad": 0.0917576456036644,
  "peak_wheel_torque_nm": 1.8532830476760864,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.12260102511861933,
  "final_integral_m_s": -0.12260102511861933,
  "elapsed_wall_s": 8.889210394991096
}
```
