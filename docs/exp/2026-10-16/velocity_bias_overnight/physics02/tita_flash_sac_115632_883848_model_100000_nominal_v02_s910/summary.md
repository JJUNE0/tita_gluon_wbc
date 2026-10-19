# tita_flash_sac_115632_883848_model_100000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 8f42f54ad53cf728ae0a4f9196bf1dc677793bfdff7ab107449376398eaeae6c

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_100000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_100000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "initial_physics_sha256": "a409b7fe269c81f27a75f2c94fcd3031f992971cec4504e852c8906a7db28c63",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.05355966915651534,
  "max_drift_m": 0.06702174152197618,
  "radial_IAE_m_s": 3.1349387911828335,
  "signed_longitudinal_delta_m": 0.05355902604061329,
  "tail_speed_mean_m_s": 3.7777710257199986e-05,
  "tail_speed_rms_m_s": 3.793319723039601e-05,
  "tail_sensor_speed_mean_m_s": 3.752120192911906e-05,
  "tail_fk_speed_mean_m_s": 3.7529732897409746e-05,
  "peak_tilt_rad": 0.0849449600932477,
  "peak_wheel_torque_nm": 0.6247534155845642,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.542006436975744,
  "final_integral_m_s": 0.5419299457310245,
  "elapsed_wall_s": 11.979588281014003
}
```
