# tita_flash_sac_193248_068255_model_60000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "checkpoint_sha256": "9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b",
  "onnx_sha256": "bd80a0d28ffd69209d8e2ef2f6d867ca3f72a00abd0a3c8dbb0b6def13e19b7e",
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
  "initial_physics_sha256": "24f0f3c541f71df8dac2945a91ab94121de65f48425335a0436dac80df4fb4db",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03663446668638748,
  "max_drift_m": 0.044284847677457516,
  "radial_IAE_m_s": 2.2102564457911167,
  "signed_longitudinal_delta_m": -0.036619869524396914,
  "tail_speed_mean_m_s": 7.780230099997026e-06,
  "tail_speed_rms_m_s": 7.781332126110892e-06,
  "tail_sensor_speed_mean_m_s": 7.810101131965957e-06,
  "tail_fk_speed_mean_m_s": 7.88504698052732e-06,
  "peak_tilt_rad": 0.09938244703502752,
  "peak_wheel_torque_nm": 0.699249267578125,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.3767642754903669,
  "final_integral_m_s": -0.3767796379945356,
  "elapsed_wall_s": 16.945078509976156
}
```
