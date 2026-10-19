# tita_flash_sac_193248_068255_model_80000

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0a7e2625e498c764511b15f8f6d7500520f4d3fc133e0951436d3c2304be9168

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_80000",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_80000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 270,
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "initial_physics_sha256": "a5857e9bfda9a49bd11519a2b6052dfc2f8af8151855c751ca73c3ecb0b2e12e",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 2.6677342683738146,
  "max_drift_m": 2.6677342683738146,
  "radial_IAE_m_s": 75.91613170969357,
  "signed_longitudinal_delta_m": 2.666328575217397,
  "tail_speed_mean_m_s": 0.048846136086865444,
  "tail_speed_rms_m_s": 0.04893998215317278,
  "tail_sensor_speed_mean_m_s": 0.04850164821229238,
  "tail_fk_speed_mean_m_s": 0.0488910644034146,
  "peak_tilt_rad": 0.05427170905687895,
  "peak_wheel_torque_nm": 1.8044638633728027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 5.238613847992383
}
```
