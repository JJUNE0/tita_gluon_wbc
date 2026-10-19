# tita_flash_sac_115632_883848_model_30000_mass130_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_mass130_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "mass": 1.3
    },
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "17297fee2061fce9c518e57482c614c1ce3f6004be6932d9bf5dd3f13cf012ef",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 10.761692507774809,
  "max_drift_m": 10.761692507774809,
  "radial_IAE_m_s": 321.5308210044043,
  "signed_longitudinal_delta_m": -10.679552046786975,
  "tail_speed_mean_m_s": -0.18153267708393903,
  "tail_speed_rms_m_s": 0.18153277547640265,
  "tail_sensor_speed_mean_m_s": -0.181144176715693,
  "tail_fk_speed_mean_m_s": -0.1811383080811727,
  "peak_tilt_rad": 0.029392023068718798,
  "peak_wheel_torque_nm": 0.2877785563468933,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.769255582999904
}
```
