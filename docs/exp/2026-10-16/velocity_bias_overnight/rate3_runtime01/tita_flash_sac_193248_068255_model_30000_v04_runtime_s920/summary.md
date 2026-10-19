# tita_flash_sac_193248_068255_model_30000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 1e8eb8c4549e7335f4ef3d31ec9b7b45fd0cb148283a41b8c616f429cefb643f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_30000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_30000",
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
  "initial_physics_sha256": "d919daa39a883034fa6947da6ce24b46d9ed47a954bba01fd5032bb2248bfefa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008620253710844792,
  "max_drift_m": 0.01707543656456885,
  "radial_IAE_m_s": 0.5130696787560214,
  "signed_longitudinal_delta_m": -0.008615653838383518,
  "tail_speed_mean_m_s": -1.1797511073904016e-05,
  "tail_speed_rms_m_s": 1.4546084866109277e-05,
  "tail_sensor_speed_mean_m_s": -1.1532160973876438e-05,
  "tail_fk_speed_mean_m_s": -1.184118181715243e-05,
  "peak_tilt_rad": 0.023430380353578473,
  "peak_wheel_torque_nm": 0.3783695101737976,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.10988483172927013,
  "final_integral_m_s": 0.10988483172927013,
  "elapsed_wall_s": 12.219785509980284
}
```
