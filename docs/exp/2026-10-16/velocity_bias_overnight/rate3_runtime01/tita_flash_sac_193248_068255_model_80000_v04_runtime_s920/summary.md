# tita_flash_sac_193248_068255_model_80000_v04_runtime_s920

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_v04_runtime_s920",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
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
  "initial_physics_sha256": "f121c2ddd960733b9e9607b2b8cede31e669859e7d789509661da85f83af494b",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.06524817985485232,
  "max_drift_m": 0.06524817985485232,
  "radial_IAE_m_s": 3.6794614842487663,
  "signed_longitudinal_delta_m": 0.06524744680897632,
  "tail_speed_mean_m_s": 5.939919214697894e-05,
  "tail_speed_rms_m_s": 5.9638454696974795e-05,
  "tail_sensor_speed_mean_m_s": 5.8909766910574225e-05,
  "tail_fk_speed_mean_m_s": 6.0366065656125655e-05,
  "peak_tilt_rad": 0.0526649679739184,
  "peak_wheel_torque_nm": 2.23673152923584,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18164647903772096,
  "final_integral_m_s": 0.18164647903772096,
  "elapsed_wall_s": 12.461498235003091
}
```
