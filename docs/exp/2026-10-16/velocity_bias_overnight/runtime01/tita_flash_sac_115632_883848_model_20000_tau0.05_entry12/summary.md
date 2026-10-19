# tita_flash_sac_115632_883848_model_20000_tau0.05_entry12

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_tau0.05_entry12",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 271,
    "estimator": "fk",
    "runtime": true,
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
  "initial_physics_sha256": "c018fb58bcdb6e0ea6f9209653883ea8c1af375ddd076ab1b7f47700e0639962",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.02377212699876718,
  "max_drift_m": 0.0694902653291196,
  "radial_IAE_m_s": 1.4609502548019089,
  "signed_longitudinal_delta_m": 0.023772083704858244,
  "tail_speed_mean_m_s": 1.9173555089068468e-07,
  "tail_speed_rms_m_s": 3.908586536277385e-06,
  "tail_sensor_speed_mean_m_s": 6.355682763463939e-06,
  "tail_fk_speed_mean_m_s": 1.4120288946996555e-05,
  "peak_tilt_rad": 0.1533003240660673,
  "peak_wheel_torque_nm": 1.0653724670410156,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.2695431932082975,
  "final_integral_m_s": 0.2695208724814406,
  "elapsed_wall_s": 5.911097136035096
}
```
