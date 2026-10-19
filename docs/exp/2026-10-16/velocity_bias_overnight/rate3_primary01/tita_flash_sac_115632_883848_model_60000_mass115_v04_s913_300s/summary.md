# tita_flash_sac_115632_883848_model_60000_mass115_v04_s913_300s

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_60000_mass115_v04_s913_300s",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_60000",
    "duration": 300.0,
    "warmup": 1.2,
    "seed": 913,
    "estimator": "fk",
    "physics": {
      "mass": 1.15
    },
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
  "checkpoint_sha256": "6d3cba9fa76eebe9fb2f40ef23d34115b8b95028ec788571531ffb33ce821a05",
  "onnx_sha256": "f44f07ed44970e3ff565eae67fd9229adf0be5c02215591c52a691ffcbb71b2a",
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
  "initial_physics_sha256": "de102d7b611657224b65a0cfa5b6c6a8b03b2ba0da773d30b4afd17f4b348517",
  "complete": true,
  "failure": [],
  "duration_s": 300.0,
  "final_drift_m": 0.005612104763663956,
  "max_drift_m": 0.034806710259776025,
  "radial_IAE_m_s": 0.9386047014697343,
  "signed_longitudinal_delta_m": -0.005567640392071686,
  "tail_speed_mean_m_s": 5.336717319159868e-06,
  "tail_speed_rms_m_s": 5.357077117029191e-06,
  "tail_sensor_speed_mean_m_s": 4.875934437880859e-06,
  "tail_fk_speed_mean_m_s": 5.972144325113582e-06,
  "peak_tilt_rad": 0.11443950889892629,
  "peak_wheel_torque_nm": 0.6568183898925781,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.25197504026929035,
  "final_integral_m_s": -0.25197504026929035,
  "elapsed_wall_s": 86.91627103695646
}
```
