# tita_flash_sac_193248_068255_model_45000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "mass": 1.15
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
  "initial_physics_sha256": "006eb2c132c91e741a60543ae9946f4ea9ee8e1878e53d3449bbf26e19b67fee",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0407998881916819,
  "max_drift_m": 0.07022135750411618,
  "radial_IAE_m_s": 2.46000075611553,
  "signed_longitudinal_delta_m": -0.04079947422727837,
  "tail_speed_mean_m_s": 2.2869746453655986e-06,
  "tail_speed_rms_m_s": 2.288214099790379e-06,
  "tail_sensor_speed_mean_m_s": 2.4662855226784977e-06,
  "tail_fk_speed_mean_m_s": 1.5234291438830988e-07,
  "peak_tilt_rad": 0.12233808680669478,
  "peak_wheel_torque_nm": 0.9781352281570435,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.4265827649454293,
  "final_integral_m_s": -0.4265829603566721,
  "elapsed_wall_s": 17.247313212952577
}
```
