# tita_flash_sac_193248_068255_model_80000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "initial_physics_sha256": "0f6fefdab08928bf1c77edc8271bba59b6e92064034a947e69c0e5958b26dacd",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.07305631372652846,
  "max_drift_m": 0.07305631372652846,
  "radial_IAE_m_s": 20.470326901375685,
  "signed_longitudinal_delta_m": 0.07304830572458051,
  "tail_speed_mean_m_s": 1.584479409329966e-05,
  "tail_speed_rms_m_s": 1.6467535655060926e-05,
  "tail_sensor_speed_mean_m_s": 1.5873937042724364e-05,
  "tail_fk_speed_mean_m_s": 1.673872870808027e-05,
  "peak_tilt_rad": 0.052674166311220016,
  "peak_wheel_torque_nm": 2.237335443496704,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.21340346319660078,
  "final_integral_m_s": 0.21340346319660078,
  "elapsed_wall_s": 26.68431593501009
}
```
