# tita_flash_sac_193248_068255_model_60000_mass130_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass130_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
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
  "initial_physics_sha256": "34ef357e300d56e0a8d158333a400732cae3851032fe0e8a1fdf5c48b3d19bf5",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.057751448103299796,
  "max_drift_m": 0.07796959908739416,
  "radial_IAE_m_s": 3.4637883210508553,
  "signed_longitudinal_delta_m": -0.057724810757631105,
  "tail_speed_mean_m_s": -2.6978800832747274e-07,
  "tail_speed_rms_m_s": 3.245057029442053e-07,
  "tail_sensor_speed_mean_m_s": -2.4825311900328024e-07,
  "tail_fk_speed_mean_m_s": -1.4552338383055626e-07,
  "peak_tilt_rad": 0.17860254366345774,
  "peak_wheel_torque_nm": 1.1898036003112793,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.5999380383863776,
  "final_integral_m_s": -0.5999378419346392,
  "elapsed_wall_s": 20.595584087946918
}
```
