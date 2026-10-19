# tita_flash_sac_193248_068255_model_10000_mass115_v02_s910

Execution Domain: VALIDATION_SIM

Policy Checkpoint SHA256: e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec

Evidence Status: PASS

Observed metrics / behavior / log summary:

```json
{
  "execution_domain": "VALIDATION_SIM",
  "evidence_status": "PASS",
  "job": {
    "id": "tita_flash_sac_193248_068255_model_10000_mass115_v02_s910",
    "checkpoint_id": "tita_flash_sac_193248_068255_model_10000",
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
  "checkpoint_sha256": "e224ae18a95522127126a105d021233677c10d5e6500107bf569c66927000bec",
  "onnx_sha256": "93a951232d50aec538c5ed480dd411ddb441d74992906cba2ee1d28d65b01670",
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
  "initial_physics_sha256": "eab24717c21b8110a62f992be4a08bb7ae5638967ffb6153a3a5e516615ee635",
  "complete": true,
  "failure": [],
  "duration_s": 60.0,
  "final_drift_m": 0.03433093713714465,
  "max_drift_m": 0.03509838887058348,
  "radial_IAE_m_s": 2.0366918197240307,
  "signed_longitudinal_delta_m": -0.034326114185275605,
  "tail_speed_mean_m_s": 1.0523420283021144e-05,
  "tail_speed_rms_m_s": 1.052518355452462e-05,
  "tail_sensor_speed_mean_m_s": 1.0669428583121889e-05,
  "tail_fk_speed_mean_m_s": 1.3388571264751013e-05,
  "peak_tilt_rad": 0.06621448515741446,
  "peak_wheel_torque_nm": 1.036537528038025,
  "saturation_fraction": 0.0,
  "final_velocity_bias_m_s": -0.34615998801659714,
  "final_integral_m_s": -0.3461861218437355,
  "elapsed_wall_s": 18.810020617034752
}
```
