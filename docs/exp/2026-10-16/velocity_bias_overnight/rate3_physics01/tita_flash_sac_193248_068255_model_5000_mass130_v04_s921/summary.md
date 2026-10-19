# tita_flash_sac_193248_068255_model_5000_mass130_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_5000_mass130_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_5000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "mass": 1.3
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
  "checkpoint_sha256": "0c6ce2fc849b775f8b54d68c5d62b070104e18f4036bbfa1d259bf96543c3f65",
  "onnx_sha256": "0db9e18936f3f631b4beff658e5d721600ad74d65fe6401c55ff3c8c9fa7b2ea",
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
  "initial_physics_sha256": "a3dbb9e750baa2b4e59f99c861608e24b98d9977d2b1a535b47c233da24dd16d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.1744684496778819,
  "max_drift_m": 0.17681550898899562,
  "radial_IAE_m_s": 10.316484159868125,
  "signed_longitudinal_delta_m": -0.17446843821360328,
  "tail_speed_mean_m_s": 4.162008873597816e-05,
  "tail_speed_rms_m_s": 4.1667231985582355e-05,
  "tail_sensor_speed_mean_m_s": 2.660771660579313e-05,
  "tail_fk_speed_mean_m_s": 2.0709242898618517e-05,
  "peak_tilt_rad": 0.14724704646117126,
  "peak_wheel_torque_nm": 3.1610379219055176,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -1.2652921738646739,
  "final_integral_m_s": -1.2652921738646739,
  "elapsed_wall_s": 12.402100997976959
}
```
