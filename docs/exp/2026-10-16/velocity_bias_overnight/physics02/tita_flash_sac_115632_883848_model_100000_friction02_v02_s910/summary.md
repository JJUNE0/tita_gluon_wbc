# tita_flash_sac_115632_883848_model_100000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    }
  },
  "checkpoint_sha256": "8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c",
  "onnx_sha256": "080dcd620db33efd066b45dd96304addfd5e8874beb155a08da4e59dfe005ec0",
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
  "initial_physics_sha256": "70ed5ef771cb639e8e62f7a3d5e3d522893735e9d8d8d285b81837a51d7f15ac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.051322964432376966,
  "max_drift_m": 0.06549317289648189,
  "radial_IAE_m_s": 3.083998648630883,
  "signed_longitudinal_delta_m": 0.051315761172337916,
  "tail_speed_mean_m_s": 1.0668415227244439e-05,
  "tail_speed_rms_m_s": 1.0714227927007095e-05,
  "tail_sensor_speed_mean_m_s": 1.019157868186807e-05,
  "tail_fk_speed_mean_m_s": 1.0563899384329886e-05,
  "peak_tilt_rad": 0.08100184307470659,
  "peak_wheel_torque_nm": 1.3570172786712646,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5339744773940461,
  "final_integral_m_s": 0.5339562738918923,
  "elapsed_wall_s": 11.22006253595464
}
```
