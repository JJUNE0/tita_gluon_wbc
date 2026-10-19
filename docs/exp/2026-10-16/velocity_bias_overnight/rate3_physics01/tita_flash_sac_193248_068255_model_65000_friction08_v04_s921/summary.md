# tita_flash_sac_193248_068255_model_65000_friction08_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_65000_friction08_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_65000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.8
    },
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 3.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f"
  },
  "checkpoint_sha256": "950b5958dfae8344a2f3cfbf5d26f83d6cac60eaaf404962bb8ea0b163f7244e",
  "onnx_sha256": "a1f326d5979e91ea8e5b962f09eb3e8da4d889ac9902563756ff9179048872c8",
  "input_columns": [
    "velocity_bias_m_s",
    "filtered_velocity_m_s",
    "integral_m_s"
  ],
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
  "initial_physics_sha256": "f2d07abd8bd53784d9a530a08d25884c96efe0739e264f7ce614eeece2380127",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.017527833296814174,
  "max_drift_m": 0.036257588661807706,
  "radial_IAE_m_s": 1.1458834689349928,
  "signed_longitudinal_delta_m": -0.017514495562150047,
  "tail_speed_mean_m_s": 3.716511006902947e-05,
  "tail_speed_rms_m_s": 3.718562733987092e-05,
  "tail_sensor_speed_mean_m_s": 3.835244441584201e-05,
  "tail_fk_speed_mean_m_s": 4.014894082719607e-05,
  "peak_tilt_rad": 0.04983461528896549,
  "peak_wheel_torque_nm": 0.24834144115447998,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.19723825054389513,
  "final_integral_m_s": -0.19723825054389513,
  "elapsed_wall_s": 9.530479454959277
}
```
