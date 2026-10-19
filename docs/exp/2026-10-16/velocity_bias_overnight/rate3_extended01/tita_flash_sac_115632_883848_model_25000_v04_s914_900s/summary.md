# tita_flash_sac_115632_883848_model_25000_v04_s914_900s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_25000_v04_s914_900s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_25000",
    "duration": 900.0,
    "warmup": 1.2,
    "seed": 914,
    "estimator": "fk",
    "runtime": true,
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
    "harness_source_sha256": "44732edc64c4d464d1589b9c6f1750ea05fedf9b89dd940c8c05058777d5240f",
    "controller_source_sha256": "4e549f65ed2d2f9b18e668a01f29676c85b4cabf11d295c503fd83ad71b2171f"
  },
  "checkpoint_sha256": "fd99df31c9e160baa980cd421917f4536bfda16779ad79754dd3d4bf13c600b1",
  "onnx_sha256": "494320c9b871a706a00e8f350ff196243c37e61c0d12ed2ab0503ea24d273b8f",
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
  "initial_physics_sha256": "4b812bd34d609053b1d507c064f920b9ae4e59441ee42ae070bdf43bd8cae15a",
  "complete": true,
  "failure": [],
  "duration_s": 900.0,
  "final_drift_m": 0.11095517059316164,
  "max_drift_m": 0.17164630738262607,
  "radial_IAE_m_s": 88.20810446293518,
  "signed_longitudinal_delta_m": 0.06156963860877157,
  "tail_speed_mean_m_s": 3.301288922118502e-06,
  "tail_speed_rms_m_s": 3.3042533853712266e-06,
  "tail_sensor_speed_mean_m_s": -1.1493061169772833e-05,
  "tail_fk_speed_mean_m_s": -1.0353712334602509e-08,
  "peak_tilt_rad": 0.1392552226263013,
  "peak_wheel_torque_nm": 2.0484628677368164,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.9639398032721311,
  "final_integral_m_s": 0.9639398032721311,
  "elapsed_wall_s": 191.34473002998857
}
```
