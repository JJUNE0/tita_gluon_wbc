# tita_flash_sac_193248_068255_model_60000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "877befc5a3f36b5efc2e036f8a3d2d7f114eef2d3fa13230eff42ad866e9f34b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0044702110814503,
  "max_drift_m": 0.00526840756357238,
  "radial_IAE_m_s": 0.1259576204538145,
  "signed_longitudinal_delta_m": 0.004437460420836386,
  "tail_speed_mean_m_s": 8.820896980683852e-05,
  "tail_speed_rms_m_s": 8.821628548854498e-05,
  "tail_sensor_speed_mean_m_s": 8.775898460338362e-05,
  "tail_fk_speed_mean_m_s": 8.998858771859096e-05,
  "peak_tilt_rad": 0.03932742788187893,
  "peak_wheel_torque_nm": 0.13939832150936127,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.011767770508193803,
  "final_integral_m_s": -0.011767770508193803,
  "elapsed_wall_s": 12.224775869981386
}
```
