# tita_flash_sac_193248_068255_model_60000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "initial_physics_sha256": "50685a706564416fca2fd3ae10125b2cbef9eb38dde925377f76c72628b19542",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.015444230513585205,
  "max_drift_m": 0.015444230513585205,
  "radial_IAE_m_s": 2.8372745376907744,
  "signed_longitudinal_delta_m": 0.015192776162030847,
  "tail_speed_mean_m_s": 2.3654852203711256e-05,
  "tail_speed_rms_m_s": 2.3680624309900083e-05,
  "tail_sensor_speed_mean_m_s": 2.3292850894704275e-05,
  "tail_fk_speed_mean_m_s": 2.5382882690298287e-05,
  "peak_tilt_rad": 0.039425239864982586,
  "peak_wheel_torque_nm": 0.14056938886642456,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.03357359164845652,
  "final_integral_m_s": 0.03357359164845652,
  "elapsed_wall_s": 26.86007034801878
}
```
