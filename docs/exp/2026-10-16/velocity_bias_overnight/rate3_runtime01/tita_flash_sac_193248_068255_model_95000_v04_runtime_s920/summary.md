# tita_flash_sac_193248_068255_model_95000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_95000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_95000",
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
  "checkpoint_sha256": "a9ca81d693e2ee34f29bbb8746ae6c7a09f1a201d1d579d15a861fab83818441",
  "onnx_sha256": "7e9315ab3ff8de6c69ba7599d9f20f2c432877c181d5c6228d4b55646de7b449",
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
  "initial_physics_sha256": "acc8ca42ec62915bb9da63fd3993a3da811f95b847d24c97aed6c2c5fd838e0c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013536904191880103,
  "max_drift_m": 0.08434789316085124,
  "radial_IAE_m_s": 1.054318970772774,
  "signed_longitudinal_delta_m": 0.013532358048540444,
  "tail_speed_mean_m_s": 3.1176045250038623e-06,
  "tail_speed_rms_m_s": 2.0234774918109708e-05,
  "tail_sensor_speed_mean_m_s": 3.396985542589421e-06,
  "tail_fk_speed_mean_m_s": 2.7440711588864394e-06,
  "peak_tilt_rad": 0.0846889808800304,
  "peak_wheel_torque_nm": 0.5858672857284546,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2371310088684501,
  "final_integral_m_s": -0.2371310088684501,
  "elapsed_wall_s": 12.739702156977728
}
```
