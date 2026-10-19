# tita_flash_sac_193248_068255_model_40000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_40000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_40000",
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
  "checkpoint_sha256": "391b8791d73b9fecdb5fae3be4e3efe31b71440d770ca559d9a5a526ad37efb4",
  "onnx_sha256": "fb82f05252341f0576dd6277b7c6e5d77e7daea4d9d3f180fe72795b3f56c966",
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
  "initial_physics_sha256": "9b81a6286050c931a6b8ce2f9239ea4a8a24c95fc20158d5248da13decce2350",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.013235201426375836,
  "max_drift_m": 0.04227527913041701,
  "radial_IAE_m_s": 0.9676527882001712,
  "signed_longitudinal_delta_m": -0.01323519708843755,
  "tail_speed_mean_m_s": 7.595468099551483e-05,
  "tail_speed_rms_m_s": 7.598853083655586e-05,
  "tail_sensor_speed_mean_m_s": 7.616752669038368e-05,
  "tail_fk_speed_mean_m_s": 7.552443689511873e-05,
  "peak_tilt_rad": 0.10831937502657185,
  "peak_wheel_torque_nm": 0.8897761106491089,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2577306937400466,
  "final_integral_m_s": 0.2577306937400466,
  "elapsed_wall_s": 12.062927333987318
}
```
