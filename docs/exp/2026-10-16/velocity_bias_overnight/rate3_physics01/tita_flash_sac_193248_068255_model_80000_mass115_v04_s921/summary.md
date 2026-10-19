# tita_flash_sac_193248_068255_model_80000_mass115_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass115_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "da6d90d24989acadc38eac6864fab2e0ce4fc810a112a04bd6c8fbd6af47c16f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0008553109036058511,
  "max_drift_m": 0.0380531839893555,
  "radial_IAE_m_s": 0.40083179343549397,
  "signed_longitudinal_delta_m": -0.0008547579612463362,
  "tail_speed_mean_m_s": -0.0002263467547390826,
  "tail_speed_rms_m_s": 0.006742862328556451,
  "tail_sensor_speed_mean_m_s": 0.001181503081531813,
  "tail_fk_speed_mean_m_s": 0.00018587329913123687,
  "peak_tilt_rad": 0.09958781021240237,
  "peak_wheel_torque_nm": 3.958822727203369,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.2173961396350559,
  "final_integral_m_s": -0.2173961396350559,
  "elapsed_wall_s": 9.562388969992753
}
```
