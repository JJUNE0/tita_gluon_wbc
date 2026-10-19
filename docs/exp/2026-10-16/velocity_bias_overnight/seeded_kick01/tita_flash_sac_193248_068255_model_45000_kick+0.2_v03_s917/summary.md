# tita_flash_sac_193248_068255_model_45000_kick+0.2_v03_s917

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick+0.2_v03_s917",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 917,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "e7bb2cbef64fc1bd25398d51e6e17bd318c0ec72510dc1488cd096849eed806b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.005057004260523373,
  "max_drift_m": 0.06173295297395401,
  "radial_IAE_m_s": 0.4888721787929276,
  "signed_longitudinal_delta_m": -0.005044643664915326,
  "tail_speed_mean_m_s": 3.9971104726863175e-05,
  "tail_speed_rms_m_s": 3.997258449081196e-05,
  "tail_sensor_speed_mean_m_s": 4.083352382773821e-05,
  "tail_fk_speed_mean_m_s": 3.835494315712098e-05,
  "peak_tilt_rad": 0.07992183188859303,
  "peak_wheel_torque_nm": 1.1798150539398193,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.21169769575088523,
  "final_integral_m_s": -0.21169769575088523,
  "elapsed_wall_s": 10.04453705594642
}
```
