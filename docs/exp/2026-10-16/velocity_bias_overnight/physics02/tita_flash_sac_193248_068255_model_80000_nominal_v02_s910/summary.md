# tita_flash_sac_193248_068255_model_80000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168",
  "onnx_sha256": "5af9596f8dbde1b5e28cdde4906d69c056291a6763354ec08a4364d1f5be23b9",
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
  "initial_physics_sha256": "fbc921e7d9f1ecf7c4e0405692dc71c255f8cddfc1b12d0d2818ee98dcba3156",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.016052429774286947,
  "max_drift_m": 0.016052429774286947,
  "radial_IAE_m_s": 0.6311863093131832,
  "signed_longitudinal_delta_m": 0.01604611576532352,
  "tail_speed_mean_m_s": 0.0002326024615149088,
  "tail_speed_rms_m_s": 0.001089537319336051,
  "tail_sensor_speed_mean_m_s": 0.00018036359805252247,
  "tail_fk_speed_mean_m_s": 0.000274777116652489,
  "peak_tilt_rad": 0.04999997500391706,
  "peak_wheel_torque_nm": 2.3731536865234375,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.18562521413014088,
  "final_integral_m_s": 0.18558194036511486,
  "elapsed_wall_s": 15.374009864986874
}
```
