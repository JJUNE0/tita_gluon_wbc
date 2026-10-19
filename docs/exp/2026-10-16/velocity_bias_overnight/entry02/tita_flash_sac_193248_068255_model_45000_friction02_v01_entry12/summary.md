# tita_flash_sac_193248_068255_model_45000_friction02_v01_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_friction02_v01_entry12",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 272,
    "estimator": "fk",
    "physics": {
      "friction": 0.2
    },
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
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
  "initial_physics_sha256": "6984e21f42d3037e1ef06a0051f43604c4da6d6f9c69b736f1e3a3dcf8cb37ac",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014939487206904226,
  "max_drift_m": 0.025184314607719416,
  "radial_IAE_m_s": 0.9308168253538107,
  "signed_longitudinal_delta_m": -0.014939189347896968,
  "tail_speed_mean_m_s": 1.748989183664091e-05,
  "tail_speed_rms_m_s": 1.7489955434185454e-05,
  "tail_sensor_speed_mean_m_s": 5.562421188183463e-06,
  "tail_fk_speed_mean_m_s": 1.5117742171290339e-06,
  "peak_tilt_rad": 0.07214236975520283,
  "peak_wheel_torque_nm": 0.39666467905044556,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.16344511506501638,
  "final_integral_m_s": -0.1634481438184749,
  "elapsed_wall_s": 4.908999910985585
}
```
