# tita_flash_sac_115632_883848_model_30000_nominal_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_115632_883848_model_30000_nominal_v02_s910",
    "checkpoint_id": "tita_flash_sac_115632_883848_model_30000",
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
  "checkpoint_sha256": "ecff0682f7eaeee36f7e64c94170672ae7e912f30c8502429bab1e017f7ca17a",
  "onnx_sha256": "e68dce44a40c95e38733c80c73616e51e12114a29c11f53063c1d02eb989061e",
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
  "initial_physics_sha256": "f07a29c93293b5218116b72710e08be8c6207cc8caef81eb69981149663b2c79",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.053430717176224767,
  "max_drift_m": 0.11712194199101524,
  "radial_IAE_m_s": 3.2414040343825947,
  "signed_longitudinal_delta_m": 0.0534163841877446,
  "tail_speed_mean_m_s": -1.6036738731088817e-05,
  "tail_speed_rms_m_s": 2.2352524059462196e-05,
  "tail_sensor_speed_mean_m_s": -1.7187679314995545e-05,
  "tail_fk_speed_mean_m_s": -1.557705869971771e-05,
  "peak_tilt_rad": 0.1268433296302347,
  "peak_wheel_torque_nm": 1.116767406463623,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": 0.5614647480269479,
  "final_integral_m_s": 0.5615536464181453,
  "elapsed_wall_s": 11.567515595001169
}
```
