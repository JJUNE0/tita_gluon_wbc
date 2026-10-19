# tita_flash_sac_193248_068255_model_10000_nominal_baseline_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_nominal_baseline_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": false,
    "physics": {},
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "62b4100215c4f68354baa3af96891af659e78a35838f06e2993343f826d800a1",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.328260055147903,
  "max_drift_m": 0.328260055147903,
  "radial_IAE_m_s": 9.05940567696171,
  "signed_longitudinal_delta_m": 0.32361553348570765,
  "tail_speed_mean_m_s": 0.0062992332062442,
  "tail_speed_rms_m_s": 0.006302590951002255,
  "tail_sensor_speed_mean_m_s": 0.006306380859108516,
  "tail_fk_speed_mean_m_s": 0.006313422501497452,
  "peak_tilt_rad": 0.024645117000669035,
  "peak_wheel_torque_nm": 0.9034628868103027,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 8.971559908008203
}
```
