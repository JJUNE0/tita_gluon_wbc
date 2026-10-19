# tita_flash_sac_193248_068255_model_70000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 922,
    "estimator": "fk",
    "guarded": true,
    "kick": 0.2,
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
  "initial_physics_sha256": "00cff601d4365785efc1656053df617d6f94e14967026f0a32e76a204879e55d",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.01318589378121704,
  "max_drift_m": 0.11832558550644164,
  "radial_IAE_m_s": 0.8866341283715191,
  "signed_longitudinal_delta_m": 0.013184921524242802,
  "tail_speed_mean_m_s": 6.203565727969687e-05,
  "tail_speed_rms_m_s": 6.21806419013403e-05,
  "tail_sensor_speed_mean_m_s": 6.203095751630239e-05,
  "tail_fk_speed_mean_m_s": 6.176636997919488e-05,
  "peak_tilt_rad": 0.09642321408343002,
  "peak_wheel_torque_nm": 1.6046487092971802,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08669104687367174,
  "final_integral_m_s": 0.08669104687367174,
  "elapsed_wall_s": 10.733004160050768
}
```
