# tita_flash_sac_193248_068255_model_45000_com+0.005_v01

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 70a9e97ecbd4861ec30c17805a0e137ff6f7723b96433205dbd8c3fc0e1b103a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_45000_com+0.005_v01",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_45000",
    "duration": 60.0,
    "warmup": 8.0,
    "seed": 272,
    "physics": {
      "com": 0.005
    },
    "kick": 0.0,
    "law": {
      "kp": 2.0,
      "ki": 10.0,
      "tau": 0.05,
      "ramp": 0.25,
      "sign": 1.0,
      "limit": 2.0,
      "slew": 2.0
    },
    "estimator": "fk"
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
  "initial_physics_sha256": "1156c32bb1a04878f247ea453fee08bfd897abc99d3ad136725ce7e74e7321b9",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.014523058261990789,
  "max_drift_m": 0.04196412980142954,
  "radial_IAE_m_s": 0.9205386429690441,
  "signed_longitudinal_delta_m": -0.01452299301084358,
  "tail_speed_mean_m_s": 1.7964746339516647e-05,
  "tail_speed_rms_m_s": 1.796534065535083e-05,
  "tail_sensor_speed_mean_m_s": 1.874205462752511e-05,
  "tail_fk_speed_mean_m_s": 1.6456342578569577e-05,
  "peak_tilt_rad": 0.08756295423441296,
  "peak_wheel_torque_nm": 0.8119508624076843,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.1593535408383347,
  "final_integral_m_s": -0.15938583269946102,
  "elapsed_wall_s": 5.561897229985334
}
```
