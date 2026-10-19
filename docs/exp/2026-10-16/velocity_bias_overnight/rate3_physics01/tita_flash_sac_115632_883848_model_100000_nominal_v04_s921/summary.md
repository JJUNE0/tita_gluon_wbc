# tita_flash_sac_115632_883848_model_100000_nominal_v04_s921

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_nominal_v04_s921",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
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
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "dfa3a1b01fc42eef074c67242e97108d6d52bfbd805c5e996c8e0e30e1ae3c5f",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.091344299139193,
  "max_drift_m": 0.11352176747453956,
  "radial_IAE_m_s": 5.283713925341481,
  "signed_longitudinal_delta_m": 0.09134392345294619,
  "tail_speed_mean_m_s": 9.64658428532978e-05,
  "tail_speed_rms_m_s": 9.712992582118518e-05,
  "tail_sensor_speed_mean_m_s": 9.60839310480229e-05,
  "tail_fk_speed_mean_m_s": 9.608919394686654e-05,
  "peak_tilt_rad": 0.08457160766839289,
  "peak_wheel_torque_nm": 0.46793314814567566,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.541042797475925,
  "final_integral_m_s": 0.541042797475925,
  "elapsed_wall_s": 10.429890504979994
}
```
