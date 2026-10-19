# tita_flash_sac_115632_883848_model_70000_friction02_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_70000_friction02_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_70000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 921,
    "estimator": "fk",
    "guarded": true,
    "physics": {
      "friction": 0.2
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
  "checkpoint_sha256": "936b61280fdba31580b4cf5aba54af156eb78294655bbd493f8650181c2dd189",
  "onnx_sha256": "70370bc52ceb9baf1dff730e385c0d358159b39521a99f56af139ca34bbdccf1",
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
  "initial_physics_sha256": "f05f905f09f4d6999bae99c5c3c69aa2cfb196c17af0128ba2fb1030c0336f40",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0008284683936810793,
  "max_drift_m": 0.02397848635166088,
  "radial_IAE_m_s": 0.09665620355754875,
  "signed_longitudinal_delta_m": 0.00038690881194370643,
  "tail_speed_mean_m_s": -1.4014852753135545e-06,
  "tail_speed_rms_m_s": 2.3860931826221135e-06,
  "tail_sensor_speed_mean_m_s": -1.3894174867838122e-06,
  "tail_fk_speed_mean_m_s": -1.532678608986748e-06,
  "peak_tilt_rad": 0.03845454772394996,
  "peak_wheel_torque_nm": 0.3527570366859436,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1225665187820106,
  "final_integral_m_s": -0.1225665187820106,
  "elapsed_wall_s": 9.737854862993117
}
```
