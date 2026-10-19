# tita_flash_sac_115632_883848_model_45000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: 43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_45000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_45000",
    "duration": 60.0,
    "warmup": 1.2,
    "seed": 910,
    "estimator": "fk",
    "runtime": true,
    "physics": {},
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
  "checkpoint_sha256": "43062a7c7858bfeb0cce0542eb1f4a18dfcde51a093f58d89c7806ec35643067",
  "onnx_sha256": "7b25c8c9afe56cdbfe483aa15167008f11b20e96722bf811b19fa3d80bf0e8e5",
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
  "initial_physics_sha256": "dc6f3627330a3ae8592862b8dfc9abe5e0cb72b8b6c12ce0c40ada007c681c17",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.0046398078915951815,
  "max_drift_m": 0.014267752115240402,
  "radial_IAE_m_s": 0.5036891101982462,
  "signed_longitudinal_delta_m": 0.0037662072873483102,
  "tail_speed_mean_m_s": -0.00021826866824400468,
  "tail_speed_rms_m_s": 0.00899473223887256,
  "tail_sensor_speed_mean_m_s": -0.0019010798647380682,
  "tail_fk_speed_mean_m_s": 5.705186283961648e-05,
  "peak_tilt_rad": 0.04342044795101074,
  "peak_wheel_torque_nm": 3.4080629348754883,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.16741135379325847,
  "final_integral_m_s": 0.14689017086824652,
  "elapsed_wall_s": 11.417663497966714
}
```
