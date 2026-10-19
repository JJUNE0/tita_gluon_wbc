# tita_flash_sac_193248_068255_model_30000_mass115_v03_s916

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_mass115_v03_s916",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 916,
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
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
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
  "initial_physics_sha256": "ecfdb6209bb1c16ba118f8dcd568c1913eec9de03ada76a79e0742ba57b6fbb3",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.007285608621212536,
  "max_drift_m": 0.021192949550221208,
  "radial_IAE_m_s": 0.4647416086101499,
  "signed_longitudinal_delta_m": 0.0072855937370541,
  "tail_speed_mean_m_s": -7.493532989131782e-06,
  "tail_speed_rms_m_s": 7.506976032175914e-06,
  "tail_sensor_speed_mean_m_s": -7.288374995383707e-06,
  "tail_fk_speed_mean_m_s": -7.3946036974237855e-06,
  "peak_tilt_rad": 0.06115749702166684,
  "peak_wheel_torque_nm": 0.5943945646286011,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.13221234851210353,
  "final_integral_m_s": -0.13221234851210353,
  "elapsed_wall_s": 10.412205585977063
}
```
