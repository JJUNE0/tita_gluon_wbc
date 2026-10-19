# tita_flash_sac_193248_068255_model_45000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
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
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "f6c9f8f19e1f87707d41c52e867dbc28cb9c90a5fdc24195bd92da0b6cf1271f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005813847954988207,
  "max_drift_m": 0.04363783275384517,
  "radial_IAE_m_s": 0.4726436681050841,
  "signed_longitudinal_delta_m": -0.005808851762516451,
  "tail_speed_mean_m_s": 3.965566676704113e-05,
  "tail_speed_rms_m_s": 3.965735331088514e-05,
  "tail_sensor_speed_mean_m_s": 4.050026295844552e-05,
  "tail_fk_speed_mean_m_s": 3.801895463987399e-05,
  "peak_tilt_rad": 0.08066619087234739,
  "peak_wheel_torque_nm": 0.46391549706459045,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2107970679186163,
  "final_integral_m_s": -0.2107970679186163,
  "elapsed_wall_s": 12.547404338954948
}
```
