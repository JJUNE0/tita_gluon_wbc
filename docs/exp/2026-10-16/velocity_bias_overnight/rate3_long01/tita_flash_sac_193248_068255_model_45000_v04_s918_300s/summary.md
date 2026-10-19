# tita_flash_sac_193248_068255_model_45000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 918,
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
  "final_drift_m": 0.002149694829988436,
  "max_drift_m": 0.04389035556291939,
  "radial_IAE_m_s": 1.059581380391671,
  "signed_longitudinal_delta_m": 0.001766741359404728,
  "tail_speed_mean_m_s": 2.8350732641886376e-05,
  "tail_speed_rms_m_s": 2.8352109450842628e-05,
  "tail_sensor_speed_mean_m_s": 2.8537774294157756e-05,
  "tail_fk_speed_mean_m_s": 2.619925364201273e-05,
  "peak_tilt_rad": 0.08079345623990464,
  "peak_wheel_torque_nm": 0.4663539230823517,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.18273961748016632,
  "final_integral_m_s": -0.18273961748016632,
  "elapsed_wall_s": 31.38570703199366
}
```
