# tita_flash_sac_115632_883848_model_20000_com_plus5mm_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_com_plus5mm_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {
      "com": 0.005
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
  "initial_physics_sha256": "d4909878277d3c13aa185d3adae77e7883a9250fe22bef90f49a684bb011b3c2",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.030879984785363572,
  "max_drift_m": 0.09200331786199016,
  "radial_IAE_m_s": 1.9161506083887594,
  "signed_longitudinal_delta_m": 0.03086031541648251,
  "tail_speed_mean_m_s": -2.1785641373854074e-05,
  "tail_speed_rms_m_s": 2.227532497719368e-05,
  "tail_sensor_speed_mean_m_s": -1.291784485969217e-05,
  "tail_fk_speed_mean_m_s": -4.091389777320031e-06,
  "peak_tilt_rad": 0.16207311087723664,
  "peak_wheel_torque_nm": 1.0716816186904907,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.34494619446385116,
  "final_integral_m_s": 0.3449556094179553,
  "elapsed_wall_s": 12.792966932989657
}
```
