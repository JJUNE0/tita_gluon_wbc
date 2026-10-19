# tita_flash_sac_115632_883848_model_20000_v04_s918_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_20000_v04_s918_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_20000",
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
  "checkpoint_sha256": "c067f9f1969ee73b6c4bffcaac2a22db6c94c15ed22bacc3ce5bbde40776fe1b",
  "onnx_sha256": "3239fc95c745b5b2f5eed89d510784b637873c36570ad233e58125f30736faf4",
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
  "initial_physics_sha256": "76e3ee49bb2a73977ec541d378239579ec194398c4465b12e7f5b6e51b76770d",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.030353246426130565,
  "max_drift_m": 0.09845536880952908,
  "radial_IAE_m_s": 8.976545971634351,
  "signed_longitudinal_delta_m": -0.02845966888601881,
  "tail_speed_mean_m_s": 3.0090994388092892e-05,
  "tail_speed_rms_m_s": 3.107380892859883e-05,
  "tail_sensor_speed_mean_m_s": -0.00014781518159315534,
  "tail_fk_speed_mean_m_s": 1.3063846934955583e-06,
  "peak_tilt_rad": 0.1528544494686459,
  "peak_wheel_torque_nm": 1.0045647621154785,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.3843647587413042,
  "final_integral_m_s": 0.3843647587413042,
  "elapsed_wall_s": 82.78502097795717
}
```
