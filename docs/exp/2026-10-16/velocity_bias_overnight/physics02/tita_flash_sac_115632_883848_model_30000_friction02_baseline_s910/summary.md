# tita_flash_sac_115632_883848_model_30000_friction02_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_friction02_baseline_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {
      "friction": 0.2
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
  "initial_physics_sha256": "bf3e5e71f6cca5c18334a5f4e30b104f2529276bd1b815f045693752d53722b1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 13.616538868019756,
  "max_drift_m": 13.616538868019756,
  "radial_IAE_m_s": 407.1558758336443,
  "signed_longitudinal_delta_m": 13.361582858630703,
  "tail_speed_mean_m_s": 0.22983801839145432,
  "tail_speed_rms_m_s": 0.2298380770485959,
  "tail_sensor_speed_mean_m_s": 0.22933026244236,
  "tail_fk_speed_mean_m_s": 0.2293275143307703,
  "peak_tilt_rad": 0.10761107341646525,
  "peak_wheel_torque_nm": 0.08990335464477539,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 10.016860074014403
}
```
