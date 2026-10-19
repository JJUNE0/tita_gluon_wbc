# tita_flash_sac_193248_068255_model_80000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "e5ef314e33706dfccfa7e2bffc826ac1065299098cb20db40558a47d180c2cd4",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.039046322640112846,
  "max_drift_m": 0.039046322640112846,
  "radial_IAE_m_s": 1.744013937946168,
  "signed_longitudinal_delta_m": -0.03904325065143759,
  "tail_speed_mean_m_s": -0.0003627379337307991,
  "tail_speed_rms_m_s": 0.007453412745089874,
  "tail_sensor_speed_mean_m_s": -0.0013217865353778954,
  "tail_fk_speed_mean_m_s": 5.380991342145391e-05,
  "peak_tilt_rad": 0.10122492087573165,
  "peak_wheel_torque_nm": 4.548094272613525,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18231082084348477,
  "final_integral_m_s": -0.21286908690089,
  "elapsed_wall_s": 16.2037191229756
}
```
