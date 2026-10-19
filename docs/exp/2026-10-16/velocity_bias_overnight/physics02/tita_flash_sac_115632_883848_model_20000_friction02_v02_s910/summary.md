# tita_flash_sac_115632_883848_model_20000_friction02_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_friction02_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "fc2866593abd14adb74ac57eeff641f9a4f969cd0f694fe8252b758331dc67fc",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.054135019069214585,
  "max_drift_m": 0.09400067786250288,
  "radial_IAE_m_s": 3.299536287886436,
  "signed_longitudinal_delta_m": 0.05392648597589661,
  "tail_speed_mean_m_s": 9.917174647276132e-05,
  "tail_speed_rms_m_s": 9.917276261528931e-05,
  "tail_sensor_speed_mean_m_s": -0.00033600139114897367,
  "tail_fk_speed_mean_m_s": -1.0916429984195715e-07,
  "peak_tilt_rad": 0.16533433282421983,
  "peak_wheel_torque_nm": 0.8602578043937683,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5095006180755682,
  "final_integral_m_s": 0.5095010102610008,
  "elapsed_wall_s": 12.157079776981845
}
```
