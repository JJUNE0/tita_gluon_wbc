# tita_flash_sac_193248_068255_model_25000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_25000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_25000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "a88ec2159129b2c9f29715b2f942b238e93417aa23bf3fefea0bf1d4336216e5",
  "onnx_sha256": "19391bfb486479152b3d34f022849e6a9a0c6ba15be2cb35b847b19256f6e30b",
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
  "initial_physics_sha256": "eec166a3ebe27ce9d52142c017fdbeeecb569867d5b291b865557c051486d8ff",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007986664123614002,
  "max_drift_m": 0.022971755478933768,
  "radial_IAE_m_s": 0.4001437648062332,
  "signed_longitudinal_delta_m": -0.007986000092714867,
  "tail_speed_mean_m_s": -4.275441519862173e-05,
  "tail_speed_rms_m_s": 4.290877920045253e-05,
  "tail_sensor_speed_mean_m_s": -4.218979746227651e-05,
  "tail_fk_speed_mean_m_s": -4.3283321147969815e-05,
  "peak_tilt_rad": 0.1372408174327926,
  "peak_wheel_torque_nm": 0.5926238298416138,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.17760575978155016,
  "final_integral_m_s": -0.17760575978155016,
  "elapsed_wall_s": 9.55705213098554
}
```
