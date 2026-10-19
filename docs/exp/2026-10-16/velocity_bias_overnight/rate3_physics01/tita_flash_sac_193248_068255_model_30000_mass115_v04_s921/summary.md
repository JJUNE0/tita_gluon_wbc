# tita_flash_sac_193248_068255_model_30000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.15
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
  "checkpoint_sha256": "1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f",
  "onnx_sha256": "ec18f72b80fd3755cb0dce2de3434e16c4375a38100a8a08c28560539614d4a8",
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
  "initial_physics_sha256": "488bb33bba246380c13bdbd5396ec1ec4343e33bed7a5620acde68b9decb47b8",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007285579358505762,
  "max_drift_m": 0.0211929240007135,
  "radial_IAE_m_s": 0.46474210684303885,
  "signed_longitudinal_delta_m": 0.0072855644707947274,
  "tail_speed_mean_m_s": -7.493427802216892e-06,
  "tail_speed_rms_m_s": 7.50598507763231e-06,
  "tail_sensor_speed_mean_m_s": -7.289644418890419e-06,
  "tail_fk_speed_mean_m_s": -7.394900846748293e-06,
  "peak_tilt_rad": 0.061157482831669885,
  "peak_wheel_torque_nm": 0.594395637512207,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.13221247764109115,
  "final_integral_m_s": -0.13221247764109115,
  "elapsed_wall_s": 9.685382060997654
}
```
