# tita_flash_sac_193248_068255_model_45000_v03_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_v03_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
    "estimator": "fk",
    "guarded": true,
    "law": {
      "kp": 0.0,
      "ki": 4.0,
      "tau": 0.1,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0,
      "seed_gain": 3.0
    },
    "harness_source_sha256": "4ff3ecd43736e7421886fef49ea6c298876e4db05558b72cc28d5308763fb7a0"
  },
  "checkpoint_sha256": "70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a",
  "onnx_sha256": "f6bd5f1e2f31278db9eb7cc34e33c35b26407a27d2b9d587a0443c3dc0ab4bb8",
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
  "initial_physics_sha256": "81719af94f0f0d6ea89f765c5c33fc2e15783ac890264e85db0058f7b049a520",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.002149696630165674,
  "max_drift_m": 0.04389034492937295,
  "radial_IAE_m_s": 1.05958131504619,
  "signed_longitudinal_delta_m": 0.0017667462997712296,
  "tail_speed_mean_m_s": 2.8349893805602108e-05,
  "tail_speed_rms_m_s": 2.835131756136399e-05,
  "tail_sensor_speed_mean_m_s": 2.853632875671158e-05,
  "tail_fk_speed_mean_m_s": 2.619865892413977e-05,
  "peak_tilt_rad": 0.08079343479837386,
  "peak_wheel_torque_nm": 0.4663471579551697,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18273967706988775,
  "final_integral_m_s": -0.18273967706988775,
  "elapsed_wall_s": 51.34548073500628
}
```
