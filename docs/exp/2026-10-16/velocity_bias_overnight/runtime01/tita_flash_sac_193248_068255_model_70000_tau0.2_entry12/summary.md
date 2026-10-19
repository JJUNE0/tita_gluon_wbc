# tita_flash_sac_193248_068255_model_70000_tau0.2_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_70000_tau0.2_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.2,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "e439f20c11a536f9853e4c13fe7127d3c2bbeba319ef7a99ce8cd3071d8c3d58",
  "onnx_sha256": "69ed1a24755409f08a0de53dcb6bb767281a855b722e0c6e9fd6af7a63848138",
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
  "initial_physics_sha256": "c5ede8f600b02438938815a157985680d7dea91a9e4739b0d8ad0c9e256455fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.008346134149079164,
  "max_drift_m": 0.011488730600725961,
  "radial_IAE_m_s": 0.4495395852178229,
  "signed_longitudinal_delta_m": 0.008346106378575767,
  "tail_speed_mean_m_s": 2.7203639605847205e-05,
  "tail_speed_rms_m_s": 2.738733302170366e-05,
  "tail_sensor_speed_mean_m_s": 2.727724320996953e-05,
  "tail_fk_speed_mean_m_s": 2.701827326195625e-05,
  "peak_tilt_rad": 0.07514478923258605,
  "peak_wheel_torque_nm": 0.07880892604589462,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.08514802632755973,
  "final_integral_m_s": 0.08510003374612671,
  "elapsed_wall_s": 13.596623104007449
}
```
