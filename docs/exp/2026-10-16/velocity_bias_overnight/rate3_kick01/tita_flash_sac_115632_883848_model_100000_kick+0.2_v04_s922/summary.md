# tita_flash_sac_115632_883848_model_100000_kick+0.2_v04_s922

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_kick+0.2_v04_s922",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
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
  "initial_physics_sha256": "35e492321a978796cbd9f7fff44961ea55d4238670b9506b4c2c53879cc19c30",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0933585387458538,
  "max_drift_m": 0.1797940313051262,
  "radial_IAE_m_s": 5.568077060229334,
  "signed_longitudinal_delta_m": 0.0933570745010749,
  "tail_speed_mean_m_s": 9.279324492305055e-05,
  "tail_speed_rms_m_s": 9.304431287965484e-05,
  "tail_sensor_speed_mean_m_s": 9.241985435154704e-05,
  "tail_fk_speed_mean_m_s": 9.24290626609483e-05,
  "peak_tilt_rad": 0.10375378651647416,
  "peak_wheel_torque_nm": 2.480123519897461,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5425170072613226,
  "final_integral_m_s": 0.5425170072613226,
  "elapsed_wall_s": 7.402088404982351
}
```
