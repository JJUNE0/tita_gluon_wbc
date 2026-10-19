# tita_flash_sac_193248_068255_model_80000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
    },
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
  "initial_physics_sha256": "8e8d230ff99187af5ba390e1c9dd4ee8f289552f99e0e89eb187e4f46b24272a",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.024791202156529555,
  "max_drift_m": 0.024791202156529555,
  "radial_IAE_m_s": 1.435991010305418,
  "signed_longitudinal_delta_m": 0.02478169470388363,
  "tail_speed_mean_m_s": 2.0660217303676225e-05,
  "tail_speed_rms_m_s": 2.0744776106492607e-05,
  "tail_sensor_speed_mean_m_s": 2.0126087572470285e-05,
  "tail_fk_speed_mean_m_s": 2.1835163157203995e-05,
  "peak_tilt_rad": 0.05190685328362954,
  "peak_wheel_torque_nm": 2.143101453781128,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.24543069161919276,
  "final_integral_m_s": 0.24538966518988106,
  "elapsed_wall_s": 14.863587704952806
}
```
