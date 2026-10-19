# tita_flash_sac_193248_068255_model_45000_kick-0.2_baseline_s912

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_kick-0.2_baseline_s912",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 912,
    "estimator": "fk",
    "runtime": false,
    "kick": -0.2,
    "law": {
      "mode": "constant",
      "bias": 0.0
    }
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "0338938fe7acbe183f86375af3bfde2238197080c8eca272a42bd171794552fe",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 8.435177972760203,
  "max_drift_m": 8.435177972760203,
  "radial_IAE_m_s": 254.82417866559155,
  "signed_longitudinal_delta_m": -8.390447918646506,
  "tail_speed_mean_m_s": -0.1413275525764608,
  "tail_speed_rms_m_s": 0.14133014927655893,
  "tail_sensor_speed_mean_m_s": -0.14112253252810128,
  "tail_fk_speed_mean_m_s": -0.1411345662737298,
  "peak_tilt_rad": 0.03977331920590643,
  "peak_wheel_torque_nm": 1.5885504484176636,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.0,
  "final_integral_m_s": 0.0,
  "elapsed_wall_s": 13.144426095997915
}
```
