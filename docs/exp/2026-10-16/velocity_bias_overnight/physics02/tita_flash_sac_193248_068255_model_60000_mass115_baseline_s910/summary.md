# tita_flash_sac_193248_068255_model_60000_mass115_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 9b0d8897472dc567619d49df3e6df08813dcbb15b018f23ed58060e92e1b139b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_60000_mass115_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_60000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.15
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
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
  "final_drift_m": 4.865245739822382,
  "max_drift_m": 4.865245739822382,
  "radial_IAE_m_s": 146.85125693658176,
  "signed_longitudinal_delta_m": -4.847353924796744,
  "tail_speed_mean_m_s": -0.08021494924125937,
  "tail_speed_rms_m_s": 0.0802155691602607,
  "tail_sensor_speed_mean_m_s": -0.08004125114759546,
  "tail_fk_speed_mean_m_s": -0.08003832983531825,
  "peak_tilt_rad": 0.036056686274458905,
  "peak_wheel_torque_nm": 0.10848197340965271,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 15.784172410028987
}
```
