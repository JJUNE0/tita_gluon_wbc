# tita_flash_sac_115632_883848_model_90000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_90000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_90000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "4930085834f72c133d65563169762514342959361a6d71630216f5f608b0531f",
  "onnx_sha256": "1d6ffa5d91a15cf74e2abf755c367c1fb151f6e3c740618a6e1fb2fbf28f9379",
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
  "initial_physics_sha256": "490aa176539308101f85ea81b163de6171981f0e03aa7317480add478833c27c",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05261580922069794,
  "max_drift_m": 0.05764617424660812,
  "radial_IAE_m_s": 2.1529673254335138,
  "signed_longitudinal_delta_m": -0.05232989951071078,
  "tail_speed_mean_m_s": -0.00045065231962534334,
  "tail_speed_rms_m_s": 0.028591498969739285,
  "tail_sensor_speed_mean_m_s": 0.0035845803666900364,
  "tail_fk_speed_mean_m_s": 0.00015262803271220692,
  "peak_tilt_rad": 0.15233534732203435,
  "peak_wheel_torque_nm": 6.127635478973389,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1442008041928714,
  "final_integral_m_s": -0.16121099886854423,
  "elapsed_wall_s": 17.004162587982137
}
```
