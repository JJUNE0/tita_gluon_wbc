# tita_flash_sac_193248_068255_model_70000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {},
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
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "9b9c5480f33b85211ee4ddc14207fc5dd936a9eeae8882efdbbd729eaf9da7aa",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.011484097014807751,
  "max_drift_m": 0.013892033747313546,
  "radial_IAE_m_s": 0.5584842856021843,
  "signed_longitudinal_delta_m": 0.01148408674988191,
  "tail_speed_mean_m_s": 7.159546088770336e-05,
  "tail_speed_rms_m_s": 7.202726743825415e-05,
  "tail_sensor_speed_mean_m_s": 7.156978039804358e-05,
  "tail_fk_speed_mean_m_s": 7.131960186962059e-05,
  "peak_tilt_rad": 0.07500611424405501,
  "peak_wheel_torque_nm": 0.09194987267255783,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0841292363988561,
  "final_integral_m_s": 0.0841292363988561,
  "elapsed_wall_s": 8.051186921016779
}
```
